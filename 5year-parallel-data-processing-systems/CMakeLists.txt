cmake_minimum_required(VERSION 3.15)

project(mpi_labs LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(MPI REQUIRED)

add_subdirectory(lab-1)
# add_subdirectory(lab-2)
# add_subdirectory(lab-3)
