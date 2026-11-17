#include <mpi.h>
#include <iostream>
#include <cstdlib>
#include <string>


bool readInput(int argc, char* argv[], int size, int &arraySize, bool &isBenchmark, std::string *errorMessage)
{
    if (argc < 2 || argc > 3) {
        if (errorMessage) *errorMessage = "Incorrect arguments. Usage: program.exe <array-size> [--benchmark]";
        return false;
    }

    if (argc == 3) {
        std::string benchmarkValue = std::string(argv[2]);
    
        if (benchmarkValue != "--benchmark") {
            if (errorMessage) *errorMessage = "Incorrect arguments. Usage: program.exe <array-size> [--benchmark]";
            return false;
        }
    }

    arraySize = std::atoi(argv[1]);
    if (arraySize <= 0 || arraySize % size != 0) {
        if (errorMessage) *errorMessage = "Array size must be a positive integer divisible by the number of processes.";
        return false;
    }

    isBenchmark = (argc == 3);

    return true;
}


void printArray(const int* array, int length, int blockSize)
{
    for (int i = 0; i < length; ++i) {
        if (i > 0 && i % blockSize == 0) {
            std::cout << "| ";
        }

        std::cout << array[i] << ' ';
    }

    std::cout << std::endl;
}


int main(int argc, char* argv[])
{
    MPI_Init(&argc, &argv);

    int rank = 0;
    int size = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    std::string errorMessage;
    int arraySize = 0;
    bool isBenchmark;
    bool inputValid = readInput(argc, argv, size, arraySize, isBenchmark, &errorMessage);

    if (!inputValid) {
        if (rank == 0) {
            std::cerr << errorMessage << '\n';
        }

        MPI_Finalize();
        return 1;
    }


    int* sendbuf = new int[arraySize];
    int* recvbuf = new int[arraySize];
    double start, elapsed, totalTime;

    for (int i = 0; i < arraySize; ++i) {
        sendbuf[i] = rank * arraySize + i;
    }

    if (isBenchmark) {
        MPI_Barrier(MPI_COMM_WORLD);
        start = MPI_Wtime();
    }

    int blockSize = arraySize / size;
    MPI_Alltoall(sendbuf, blockSize, MPI_INT, recvbuf, blockSize, MPI_INT, MPI_COMM_WORLD);

    if (!isBenchmark)
    {
        for (int p = 0; p < size; ++p) {
            if (rank == p) {
                std::cout << "Process " << rank << ": ";
                printArray(recvbuf, arraySize, blockSize);
            }
    
            MPI_Barrier(MPI_COMM_WORLD);
        }
    }
    else
    {
        elapsed = MPI_Wtime() - start;
        MPI_Reduce(&elapsed, &totalTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
        if (rank == 0)
            std::cout << totalTime << '\n';
    }


    delete[] sendbuf;
    delete[] recvbuf;

    MPI_Finalize();
    return 0;
}