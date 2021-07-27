import os
import sys
import yaml
from pathlib import Path

def GetFilesList(yaml_path):
    cfg_f = open(yaml_path,'r')
    cfg = yaml.load(cfg_f.read(),Loader=yaml.FullLoader)

    cwd = os.getcwd()
    # print(cfg)
    # key is output file name , value is the array of the amalgamated files.
    ret = dict()
    for key,value in cfg.items():
        # Only the suffix of files name in suffix will be considered.
        ret[key] = []

        suffix = []
        if 'suffix' in value:
            suffix = value['suffix']

        for root,_,files in os.walk(os.path.join(cwd,value['directory'])):
            for f in files:
                for suf in suffix:
                    if f.endswith(suf):
                        ret[key].append(os.path.join(root,f))
    # print(ret)
    return ret



class CFile:
    def __init__(self,file_path,output_filename,input_output):
        self.file_path = file_path
        self.file_name = Path(file_path).name
        self.file_handle = open(file_path,'r')
        self.output_filename = output_filename
        self.get_dependencies(input_output)
    def get_include_file_name(self,l):
        ret = None
        if '<' in l:
            ret = l[l.find('<')+1:l.find('>')]
        elif '\"' in l:
            ret = l[l.find('\"')+1:l.rfind('\"')]
        else:
            print('Unknown #include ?',l)
            return None

        if '/' in ret:
            ret = ret[ret.rfind('/')+1:]
        return ret
        
    def get_dependencies(self,input_output):
        # dependencies_in is this file depend on other files which will be amalgamated into the same file.
        # dependencies_out is this file depend on other files which will NOT be amalgamated into the same file.
        self.dependencies_in = set()
        self.dependencies_out = set()
        for l in self.file_handle:
            if l.startswith('#include'):
                dep_file_name = self.get_include_file_name(l)
                if dep_file_name in input_output:
                    if input_output[dep_file_name] == self.output_filename:
                        self.dependencies_in.add(dep_file_name)
                    else:
                        self.dependencies_out.add(dep_file_name)

    # f is the handle of output file ;
    # files2output is a dictionary, from input files name to themselves' output files.
    def write(self,f,input_output):
        self.file_handle.seek(0)
        f.write('\n/*** start of file {0} **/\n'.format(self.file_name))
        for l in self.file_handle:
            if l.startswith('#include'):
                dep =  self.get_include_file_name(l)
                if dep in self.dependencies_in :
                    f.write('// ' + l)
                    continue
                elif dep in self.dependencies_out :
                    f.write('// ' + l)
                    f.write('#include\"{0}\"\n'.format(input_output[dep]))
                else:
                    f.write(l)
            else:
                f.write(l)
        f.write('\n/*** end of file {0} **/\n'.format(self.file_name))


#files from file name to CFile, all of them should have the same output file name.
def get_handle_sequence(files:dict):
    in_degree = dict()
    re_dependencies = dict()
    queue = []
    ret = []
    unfinished = set()
    for key, value in files.items():
        if len(value.dependencies_in) == 0:
            ret.append(key)
            queue.append(key)
        else:
            unfinished.add(key)
            in_degree[key] = len(value.dependencies_in)
            for tmp in value.dependencies_in:
                if tmp not in re_dependencies:
                    re_dependencies[tmp] = []
                re_dependencies[tmp].append(key)
    
    while len(queue) > 0:
        tmp = queue.pop()
        if tmp not in re_dependencies:
            continue
        for file_name in re_dependencies[tmp]:
            in_degree[file_name] -= 1
            if in_degree[file_name] == 0:
                queue.append(file_name)
                unfinished.remove(file_name)
                ret.append(file_name)

    return ret


if __name__ == '__main__':
    yaml_path = sys.argv[1]

    #input_output is from output(str) to input(list)
    #output_input is from input(str) to output(str) , and this only include the fils name.
    output_input = GetFilesList(yaml_path)
    input_output = dict()
    for key,value in output_input.items():
        output_filename = Path(key).name
        for tmp in value:
            input_filename = Path(tmp).name
            input_output[input_filename] = output_filename

    # from output file name to an object { input file name : CFile }
    output_input_CFile = dict()

    for key,value in output_input.items():
        output_filename = Path(key).name
        output_input_CFile[key] = dict()
        tmp_dic = output_input_CFile[output_filename] 
        for tmp in value:
            input_filename = Path(tmp).name
            tmp_dic[input_filename] = CFile(tmp,output_filename,input_output)
    
    for key,value in output_input_CFile.items():
        seq = get_handle_sequence(value)
        if len(seq) != len(value):
            print('Not allow files dependencies to each other')
            exit(0)
        f = open(key,'w+')
        for tmp in seq:
            value[tmp].write(f,input_output)
        f.close()






