# amalgamate
combine multi-cpp fils into one ;  
把多个c/c++文件合成一个;  

## Limitations ##
合成的文件中若有重复的名字则无法获得正确的输出，即使他们不再同一个路径下。  
The output is incorrect if some files have the same name, even if they are under different directories.

目前无法对声明实现分离(.h + .c/.cpp)进行合并。  
For now, it can only amalgamate the files whose functions' definition and implementation in the same file.

不允许互相依赖(相互`#include`)  
If existing files `#include` each other, the program will exit and no output.

## How It Works ##
首先读入所有要合并的文件，根据他们的#include获得依赖图，根据依赖图确定哪个文件先处理；  
处理过程中遇到#include合并的文件的语句，会忽略。  
Read all the files which need to be amalgamated.  
Get the dependency graph according to `#include ""` or `#include <>` sentences.  
We can know the handle sequence according to the dependency graph.  
If a file `#include`other amalgamated files, the `#include` sentences will be ignored.



