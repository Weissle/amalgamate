cmake_minimum_required (VERSION 2.8.11)

project (Example1)

include_directories(${CMAKE_SOURCE_DIR}/include)
aux_source_directory(${CMAKE_SOURCE_DIR}/src ALL_CPP)
add_executable(main main.cpp ${ALL_CPP})
