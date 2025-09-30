#include <iostream>
#include <cstring>
#include "compressor/FileCompressor.h"

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cout << "4 parameters needed: [compress/decompress], [algorithm], [input path], [output path]" << std::endl;
        return 1;
    }

    if (strcmp(argv[1], "compress") == 0) {
        FileCompressor::Compress(argv[3], argv[4], argv[2]);
    } else if (strcmp(argv[1], "decompress") == 0) {
        FileCompressor::Decompress(argv[3], argv[4], argv[2]);
    } else {
        std::cout << "Incorrect 1st parameter (use \"compress\" or \"decompress\")" << std::endl;
        return 1;
    }

    return 0;
}