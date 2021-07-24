# amalgamate
combine multi-cpp fils into one ;  
把多个c/c++文件合成一个;  

## Limitations ##
合成的文件中若有重复的名字则无法获得正确的输出，即使他们不再同一个路径下。  
The output is incorrect if some files have the same name, even if they are under different directories.

不允许互相依赖(相互`#include`)  
If existing files `#include` each other, the program will exit and no output.

## How It Works ##
首先读入所有要合并的文件，根据他们的#include获得依赖图，根据依赖图确定哪个文件先处理；  
处理过程中遇到#include合并的文件的语句，会忽略。  
Read all the files which need to be amalgamated.  
Get the dependency graph according to `#include ""` or `#include <>` sentences.  
We can know the handle sequence according to the dependency graph.  
If a file `#include`other amalgamated files, the `#include` sentences will be ignored.

## How To Use ##
创建一个YAML文件{0}指定需要合并的文件和输出文件名。
比如在examples中的example1：当我们在example1文件夹下运行命令`python3 amalgamate.py amalgamate.yml`所有在include/下的.h文件都会被整合到all.h中，同理all.cpp。  
Create a YMAL file {0} which contains the amalgamated files and output files.  
For example, the example1 in the folder examples.
When we run the command `python3 amalgamate.py amalgamate.yml` under the folder example1, all .h files will be amalgamated into all.h.
Similarly to the all.cpp.

`python3 amalgamate.py {0}`  

```yaml
# examples/example1/amalgamate.yml
all.h: 
  directory: include/
  suffix: ['h']
all.cpp:
  directory: src/
  suffix: ['cpp']
```



