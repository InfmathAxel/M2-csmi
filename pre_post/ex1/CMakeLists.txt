cmake_minimum_required(VERSION 2.8)

project(helloworld)

set(CMAKE_BUILD_TYPE "Release")

# Under Windows, un-comment the following line and set the `VTK_DIR' variable to
# the path where the file `VTKConfig.cmake' is located (in your installed VTK 
# source tree).

#set(VTK_DIR "C:\\Program Files\\VTK\\lib\\vtk-5.10")


include_directories(".")

add_executable(hello main.cpp)


