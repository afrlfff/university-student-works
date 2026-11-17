#include <mpi.h>
#include <cstdlib>
#include <iostream>
#include <string>
#include <random>


bool validateInput(int argc, char* argv[], std::string *errorMessage)
{
    if (argc < 2) {
        if (errorMessage) *errorMessage = "Too few arguments. Usage: program.exe <arraySize> [--benchmark]";
        return false;
    }

    if (argc > 3) {
        if (errorMessage) *errorMessage = "Too many arguments in argument list.";
        return false;
    }

    int arraySize = std::atoi(argv[1]);
    if (arraySize < 1) {
        if (errorMessage) *errorMessage = "Array size must be positive.";
        return false;
    }
    
    if (argc > 2) {
        std::string argValue = std::string(argv[2]);

        if (argValue != "--benchmark") {
            if (errorMessage) *errorMessage = "Incorrect 2nd argument value: " + argValue + ". Possible values: --benchmark";
            return false;
        }
    }

    return true;
}


void readInput(int argc, char* argv[], int &arraySize, bool &isBenchmark)
{
    arraySize = std::atoi(argv[1]);
    isBenchmark = (argc > 2) ? (true) : (false);
}


int *generateRandomArray(int min, int max, int size)
{
    int *data = new int[size];

    std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> distribution(min, max);

    for (int i = 0; i < size; ++i) {
        data[i] = distribution(generator);
    }

    return data;
}


int main(int argc, char* argv[])
{
    MPI_Init(&argc, &argv);

    int size;
    int rank;

    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    std::string errorMessage;
    bool inputValid = validateInput(argc, argv, &errorMessage);

    if (!inputValid) {
        if (rank == 0) {
            std::cerr << errorMessage << '\n';
        }

        MPI_Finalize();
        return 1;
    }

    int arraySize;
    bool isBenchmark;
    readInput(argc, argv, arraySize, isBenchmark);

    int chunkSize = arraySize / size;
    int remainder = arraySize % size;


    if (!isBenchmark)
    {
        if (rank == 0)
        {
            int* data = generateRandomArray(0, 10, arraySize);
            int* localSums = new int[size];
            int sum = 0;

            std::cout << "Array: [";
            for (int i = 0; i < arraySize; ++i) {
                std::cout << data[i] << ((i < arraySize - 1) ? (", ") : ("]\n"));
            }
            
            int ownSize = chunkSize + (0 < remainder ? 1 : 0);
            int offset = ownSize;

            // отправка равномерных срезов массива
            for (int i = 1; i < size; ++i) {
                int localSize = chunkSize + (i < remainder ? 1 : 0);
                MPI_Send(data + offset, localSize, MPI_INT, i, 0, MPI_COMM_WORLD);
                offset += localSize;
            }

            // вычисление своей суммы
            localSums[0] = 0;
            for (int i = 0; i < ownSize; ++i) {
                localSums[0] += data[i];
            }

            // получение результатов
            for (int i = 1; i < size; ++i) {
                MPI_Recv(&(localSums[i]), 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }

            // вычисление суммы
            for (int i = 0; i < size; ++i) {
                sum += localSums[i];
            }
            
            std::cout << "Sum: " << sum << '\n';

            delete[] localSums;
            delete[] data;
        }
        else
        {
            int localSize = chunkSize + (rank < remainder ? 1 : 0);
            int* data = new int[localSize];

            MPI_Recv(data, localSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            int sum = 0;
            for (int i = 0; i < localSize; ++i) {
                sum += data[i];
            }


            delete[] data;
        }
    }
    else
    {
        // 1. Выделение памяти
        int* data, *subData, *localSums;
        int sendSize, sum, offset;
        int localSum, localSize;
        double start, elapsed, totalTime;

        if (rank == 0) {
            data = generateRandomArray(0, 10, arraySize);
            localSums = new int[size];
            localSize = chunkSize + (0 < remainder ? 1 : 0);
            offset = localSize;
            sum = 0;
        } else {
            localSize = chunkSize + (rank < remainder ? 1 : 0);
            subData = new int[chunkSize + 1];
        }


        // 2. Старт отсчета
        MPI_Barrier(MPI_COMM_WORLD);
        start = MPI_Wtime();


        // 3. Обмен
        if (rank == 0)
        {
            for (int i = 1; i < size; ++i) {
                sendSize = chunkSize + (i < remainder ? 1 : 0);
                MPI_Send(data + offset, sendSize, MPI_INT, i, 0, MPI_COMM_WORLD);
                offset += sendSize;
            }

            localSums[0] = 0;
            for (int i = 0; i < localSize; ++i) {
                localSums[0] += data[i];
            }

            for (int i = 1; i < size; ++i) {
                MPI_Recv(&(localSums[i]), 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            }

            for (int i = 0; i < size; ++i) {
                sum += localSums[i];
            }
        }
        else
        {
            MPI_Recv(subData, localSize, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            localSum = 0;
            for (int i = 0; i < localSize; ++i) {
                localSum += subData[i];
            }

            MPI_Send(&localSum, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }

        
        // 4. Фиксация времени
        elapsed = MPI_Wtime() - start;
        MPI_Reduce(&elapsed, &totalTime, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
        if (rank == 0)
            std::cout << totalTime << '\n';


        // 5. Освобождение памяти
        if (rank == 0) {
            delete[] data;
            delete[] localSums;
        } else {
            delete[] subData;
        }
    }


    MPI_Finalize();
    return 0;
}