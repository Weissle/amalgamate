cmake_minimum_required (VERSION 2.8.11)

project (Example1)

include_directories(${CMAKE_SOURCE_DIR}/include)
aux_source_directory(${CMAKE_SOURCE_DIR}/src SRC_CPP)
add_executable(main main.cpp ${SRC_CPP})

add_executable(main_ama main.cpp all.cpp)