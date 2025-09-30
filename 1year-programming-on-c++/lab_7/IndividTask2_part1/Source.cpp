#include <iostream>
#include <fstream>
#include <iomanip>
#include "block.h"
#include "funcdef.h"
using namespace std;

int main() {
	Block block;
	unsigned m, n;
	unsigned linesCount;
	unsigned* LinesLength;

	setlocale(LC_ALL, "rus");

	if (!GetSizeOfBlock(&m, &n)) return 0;
	SetSizeOfBlock(&block, m, n);
	cout << "Размер блока: " << m << "x" << n << endl;

	if(!(linesCount = GetCountOfLines())) return 0;
	cout << "Количество строк в файле: " << linesCount << endl;

	LinesLength = new unsigned[linesCount];
	if (!GetlinesLength(LinesLength, linesCount)) return 0;
	cout << "Количество символов в строках: ";
	for (unsigned k = 0; k < linesCount; k++) cout << LinesLength[k] << " ";
	cout << "\n\n";

	Process(block, LinesLength, linesCount);
	delete[] LinesLength;
	return 0;
}