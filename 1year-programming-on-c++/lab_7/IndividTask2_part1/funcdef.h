#ifndef FUNCDEF_H
#define FUNCDEF_H

#include <iostream>
#include <iomanip>
#include <fstream>

using namespace std;

void OutError(fstream* fout, unsigned type);

int Min(int a, int b);

void SetSizeOfBlock(struct Block* block, unsigned m, unsigned n);

int GetSizeOfBlock(unsigned* m, unsigned* n);

int GetCountOfLines();

int GetlinesLength(unsigned* linesLength, unsigned linesCount);

int GetRowsCount(unsigned linesCount, unsigned M);

void CreateINDEXES(streampos** INDEXES, unsigned M, const unsigned indexesCount);

void ResetINDEXES(streampos** INDEXES, unsigned M, const unsigned indexesCount);

void DeleteINDEXES(streampos** INDEXES, unsigned M);

int ChangeINDEXES(fstream* fin, streampos** INDEXES, char s, unsigned j, bool flag);

int GetBlock(fstream* fin, fstream* fout1, fstream* fout2, unsigned M, unsigned N, unsigned row, unsigned column,
	unsigned* LinesLength, unsigned* CompletedLines, unsigned* completedLinesCount, unsigned linesCount, streampos** INDEXES, bool* flags);

int GetRowOfBlocks(fstream* fin, fstream* fout1, fstream* fout2, unsigned M, unsigned N, unsigned row, unsigned column,
	unsigned* LinesLength, unsigned linesCount);

void OutResult(fstream* fin, fstream* fout, streampos** INDEXES, unsigned M, unsigned N, unsigned row, unsigned j, bool flag);

int Process(struct Block block, unsigned* LinesLength, unsigned linesCount);

#endif
