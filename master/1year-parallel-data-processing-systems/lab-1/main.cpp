#include <mpi.h>
#include <cstdlib>
#include <iostream>
#include <string>


bool validateInput(int argc, char* argv[], std::string *errorMessage)
{
    if (argc < 2) {
        if (errorMessage) *errorMessage = "Too few arguments. Usage: program.exe <1|2> [--benchmark <message_count>]";
        return false;
    }

    if (argc > 4) {
        if (errorMessage) *errorMessage = "Too many arguments in argument list.  Usage: program.exe <1|2> [--benchmark <message_count>]";
        return false;
    }

    int task = std::atoi(argv[1]);
    if (task != 1 && task != 2) {
        if (errorMessage) *errorMessage = "Unknown task number: " + std::to_string(task);
        return false;
    }
    
    if (argc > 2) {
        std::string argValue = std::string(argv[2]);

        if (argValue != "--benchmark") {
            if (errorMessage) *errorMessage = "Incorrect 2nd argument value: " + argValue + ". Possible values: --benchmark";
            return false;
        }
    }

    int messageCount = 1;
    if (argc > 3) {
        messageCount = std::atoi(argv[3]);

        if (messageCount < 0) {
            if (errorMessage) *errorMessage = "Message count must be positive.";
            return false;
        }
    }

    return true;
}


void readInput(int argc, char* argv[], int &task, bool &isBenchmark, int &messageCount)
{
    task = std::atoi(argv[1]);
    isBenchmark = (argc > 2) ? (true) : (false);
    messageCount = (argc > 3) ? std::atoi(argv[3]) : 1;
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

    int task;
    bool isBenchmark;
    int messageCount;
    readInput(argc, argv, task, isBenchmark, messageCount);


    if (!isBenchmark)
    {
        if (rank == 0) {
            std::cout << rank << std::endl;
    
            for (int i = 1; i < size; ++i) {
                int receivedRank;
    
                int source = (task == 1) ? MPI_ANY_SOURCE : i;
    
                MPI_Recv(&receivedRank, 1, MPI_INT,
                         source, 0,
                         MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    
                std::cout << receivedRank << std::endl;
            }
        } else {
            MPI_Send(&rank, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
        }
    }
    else
    {
        MPI_Barrier(MPI_COMM_WORLD);
        double start = MPI_Wtime();
    
        if (rank == 0) {
            for (int i = 1; i < size; ++i) {
                for (int j = 0; j < messageCount; ++j) {
                    int receivedRank;
        
                    int source = (task == 1) ? MPI_ANY_SOURCE : i;
        
                    MPI_Recv(&receivedRank, 1, MPI_INT,
                            source, 0,
                            MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                }
            }
        } else {
            for (int j = 0; j < messageCount; ++j) {
                MPI_Send(&rank, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
            }
        }
    
        double end = MPI_Wtime();
        double elapsed = end - start;
        double total_time;
        MPI_Reduce(&elapsed, &total_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

        if (rank == 0) {
            std::cout << total_time << std::endl;
        }
    }


    MPI_Finalize();
    return 0;
}