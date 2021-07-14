import os
import sys

class CFile:
    def __init__(self,file_path,files_name):
        self.file_path = file_path
        self.file_name = file_path[file_path.rfind('/')+1:]
        self.file_handle = open(file_path,'r')
        self.get_dependencies(files_name)
    def get_include_file_path(self,l):
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
        
    def get_dependencies(self,files_name):
        self.dependencies = []
        for l in self.file_handle:
            if l.startswith('#include'):
                dep_file_name = self.get_include_file_path(l)
                if dep_file_name in files_name:
                    self.dependencies.append(dep_file_name)

    def write(self,f,files_name):
        self.file_handle.seek(0)
        f.write('\n/*** start of file {0} **/\n'.format(self.file_name))
        for l in self.file_handle:
            if l.startswith('#include') and self.get_include_file_path(l) in files_name:
                continue
            f.write(l)
        f.write('\n/*** end of file {0} **/\n'.format(self.file_name))



def get_handle_sequence(files:dict):
    in_degree = dict()
    re_dependencies = dict()
    queue = []
    ret = []
    unfinished = set()
    for key, value in files.items():
        if len(value.dependencies) == 0:
            ret.append(key)
            queue.append(key)
        else:
            unfinished.add(key)
            in_degree[key] = len(value.dependencies)
            for tmp in value.dependencies:
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

    if len(unfinished) > 0:
        print('There is not allowed file include each other')

    return ret


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    files_name = []
    paths = []
    for l in open(input_file,'r'):
        l = l.strip()
        paths.append(l)
        if '/' in l:
            l = l[l.rfind('/')+1:]
        files_name.append(l)
    
    files = dict()
    for path,file_name in zip(paths,files_name):
        files[file_name] = CFile(path,set(files_name))

    seq = get_handle_sequence(files)
    if len(seq) != len(files_name):
        exit(1)
    f = open(output_file,'w+')
    for tmp in seq:
        files[tmp].write(f,set(files_name))
    f.close()






