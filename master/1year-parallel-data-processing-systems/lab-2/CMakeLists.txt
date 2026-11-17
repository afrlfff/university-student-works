# lab-2

set(APP_NAME "mpi_app_2")

add_executable(${APP_NAME} main.cpp)

target_link_libraries(${APP_NAME} PRIVATE MPI::MPI_CXX)
