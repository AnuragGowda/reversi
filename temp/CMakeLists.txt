cmake_minimum_required(VERSION 3.26)
project(temp)

set(CMAKE_CXX_STANDARD 20)

include_directories(.)

add_executable(temp
        board_cpp.cpp
        board_cpp.h
        Rectangle.cpp
        Rectangle.h)
