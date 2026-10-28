#include "funcdef.h"
#include "block.h"

void OutError(fstream* fout, unsigned type) {
	switch (type)
	{
	case 11: // MO 1.1
		(*fout) << "ОШИБКА: не удалось открыть входной файл.\n";
	case 12: // MO 1.2
		(*fout) << "ОШИБКА: не удалось считать размеры блока.\n";
	case 13: // MO 1.3
		(*fout) << "ОШИБКА: заданы некорректные размеры блока.\n";
	default:
		break;
	}
	fout->close();
}

int Min(int a, int b) {
	if (a <= b) return a;
	else return b;
}

void SetSizeOfBlock(struct Block* block, unsigned m, unsigned n) {
	block->M = m; block->str.N = n;
}

int GetSizeOfBlock(unsigned* m, unsigned* n) {
	fstream fin, fout;
	char s;

	fout.open("out1.txt", ios::out);
	fin.open("in.txt", ios::in);
	if (!fin.is_open()) { OutError(&fout, 11); fin.close(); return 0; }
	fin << resetiosflags(ios::skipws);

	do { fin >> s; } while (s == ' ');
	if (s == '\n' || fin.eof()) { OutError(&fout, 12); fin.close(); return 0; }
	fin.unget();
	fin >> *m;
	do { fin >> s; } while (s == ' ');
	if (s == '\n' || fin.eof()) { OutError(&fout, 12); fin.close(); return 0; }
	fin.unget(); fin >> *n;

	fin.close();
	if (*n > 0 && *m > 0) { fout.close(); return 1; }
	else { OutError(&fout, 13); return 0; }
}

int GetCountOfLines() {
	fstream fin, fout;
	char s;
	unsigned count = 0;
	fout.open("out1.txt", ios::out);
	fin.open("in.txt", ios::in);
	if (!fin.is_open()) { OutError(&fout, 11); fin.close(); return 0; }

	fin << resetiosflags(ios::skipws);
	do {
		fin >> s;
		if (s == '\n' || fin.eof()) count++;
	} while (!(fin.eof()));

	fin.close(); fout.close();
	if (count < 2) return 0;
	return count;
}

int GetlinesLength(unsigned* linesLength, unsigned linesCount) {
	char s;
	unsigned i, count;
	fstream fin, fout;
	
	fout.open("out1.txt", ios::out);
	fin.open("in.txt", ios::in);
	if (!fin.is_open()) { OutError(&fout, 11); fin.close(); return 0; }
	fin << resetiosflags(ios::skipws);

	i = 0; count = 0;
	while ((i < linesCount) && (!(fin.eof()))) {
		fin >> s;
		count++;
		if (s == '\n' || fin.eof()) {
			count--;
			linesLength[i] = count;
			count = 0; i++;
		}
	}
	fin.close(); fout.close();
	return 1;
}

int GetRowsCount(unsigned linesCount, unsigned M) {
	if ((linesCount - 1) % M == 0) return ((linesCount - 1) / M);
	else return ((linesCount - 1) / M + 1);
}

void CreateINDEXES(streampos** INDEXES, unsigned M, const unsigned indexesCount) {
	for (unsigned i = 0; i < M; i++) {
		INDEXES[i] = new streampos[indexesCount];
	}
}

void ResetINDEXES(streampos** INDEXES, unsigned M, const unsigned indexesCount) {
	for (unsigned i = 0; i < M; i++) {
		for (unsigned j = 0; j < indexesCount; j++) {
			INDEXES[i][j] = -1;
		}
	}
}

void DeleteINDEXES(streampos** INDEXES, unsigned M) {
	for (unsigned i = 0; i < M; i++) {
		delete[] INDEXES[i];
	}
	delete[] INDEXES;
}

int ChangeINDEXES(fstream* fin, streampos** INDEXES, char s, unsigned j, bool flag) {
	streampos pos;
	unsigned k;
	if (!flag) k = 0;
	else k = 6;

	if (s != ' ' && s != ',')
	{
		if (INDEXES[j][k + 0] == -1)
		{
			pos = fin->tellg(); pos -= 1;
			INDEXES[j][k + 0] = pos;
			return 0;
		}
		else if (INDEXES[j][k + 2] == -1 && INDEXES[j][k + 1] != -1)
		{
			pos = fin->tellg(); pos -= 1;
			INDEXES[j][k + 2] = pos;
			return 0;
		}
		else if (s == '[' && INDEXES[j][k + 4] != -1)
		{
			pos = fin->tellg(); pos -= 1;
			INDEXES[j][k + 5] = pos;
			return 0;
		}
		else if (s == '[' && INDEXES[j][k + 2] != -1)
		{
			pos = fin->tellg(); pos -= 1;
			INDEXES[j][k + 4] = pos;
			if (INDEXES[j][k + 3] == -1) INDEXES[j][k + 3] = pos;
			return 0;
		}
	}
	else if (s == ' ')
	{
		if (INDEXES[j][k + 0] != -1 && INDEXES[j][k + 1] == -1)
		{
			pos = fin->tellg(); pos -= 1;
			INDEXES[j][k + 1] = pos;
			return 0;
		}
		else if (INDEXES[j][k + 2] != -1 && INDEXES[j][k + 3] == -1)
		{
			pos = fin->tellg(); pos -= 1;
			INDEXES[j][k + 3] = pos;
			return 0;
		}

	}

	return 0;
}

int GetBlock(fstream* fin, fstream* fout1, fstream* fout2, unsigned M, unsigned N, unsigned row, unsigned column,
	unsigned* LinesLength, unsigned* CompletedLines, unsigned* completedLinesCount, unsigned linesCount, streampos** INDEXES, bool* flags)
{
	unsigned i, j = 0;
	char s; int t;
	//streampos pos;
	cout << "Ряд " << (row + 1) << ", блок " << (column + 1) << ":\n";
	*fout1 << "Ряд " << (row + 1) << ", блок " << (column + 1) << ":\n";

	// Цикл для считывания строк из блока
	// Перед его исполнением(считыванием данной строки) каретка находится в конце предыдущей строки
	// После завершения цикла каретка будет находиться в конце последней строки текущего блока
	while (j < M) {
		i = 0;
		// Проверяем, что данная строка внутри блока не пустая
		if (!CompletedLines[j]) {
			// идём в начало строки блока
			t = 2 + column * N;
			fin->seekg(t, ios::cur);

			// Цикл для считывания символов из строки блока
			cout << "\t"; *fout1 << "\t";
			while (i < N)
			{
				*fin >> s;

				if (s == ',') flags[j] = true;
				ChangeINDEXES(fin, INDEXES, s, j, flags[j]);

				if (s != '\n' && s != '\t' && !fin->eof()) { cout << s; *fout1 << s; }
				if (s == '\n')
				{
					(*completedLinesCount)++;
					CompletedLines[j] = 1;
					OutResult(fin, fout2, INDEXES, M, N, row, j, flags[j]);
					fin->seekg(-2, ios::cur);
					break;
				}
				if (fin->eof()) {
					fin->clear();
					OutResult(fin, fout2, INDEXES, M, N, row, j, flags[j]);
					for (unsigned k = j; k < M; k++) 
					{ (*completedLinesCount)++; CompletedLines[k] = 1; }
					
					if (*completedLinesCount == M)
					{
						fin->close();
						return 0;
					}
					else
					{
						break;
					}
				}
				i++;
			}

			// возвращаемся в начало строки блока
			t = (column * N) + (i);
			fin->seekg(-t, ios::cur);

		}
		else fin->seekg(2, ios::cur);
		cout << "\n"; *fout1 << "\n";
		// на этом моменте мы находимся в начале той строки, которую считывали

		// проверяем, что текущая строка является последней в файле
		if ((row * M + (j + 1) + 1) == linesCount) {
			fin->seekg(0, ios::end);
			break;
		}
		else {
			t = LinesLength[1 + row * M + j];
			fin->seekg(t, ios::cur);
		}
		// на этом моменте мы находимся в конце той строки, которую считывали
		j++;
	}
	cout << endl; *fout1 << endl;

	return 0;
}

int GetRowOfBlocks(fstream* fin, fstream* fout1, fstream* fout2, unsigned M, unsigned N, unsigned row, unsigned column,
	unsigned* LinesLength, unsigned linesCount)
{
	int t;
	unsigned* CompletedLines = new unsigned[M]; // строки блока, которые уже считаны
	unsigned completedLinesCount;
	const unsigned indexesCount = 6 * 2; // для каждого массива два для границ типа, два для границ имени и 2 для символов '['
	streampos** INDEXES = new streampos * [M]; // массив для хранения индексов искомых позиций в файле
	bool* flags = new bool[M]; // true - в строке задано два массива, false - только один

	for (unsigned k = 0; k < M; k++) CompletedLines[k] = 0;
	for (unsigned k = 0; k < M; k++) flags[k] = false;
	CreateINDEXES(INDEXES, M, indexesCount);
	ResetINDEXES(INDEXES, M, indexesCount);
	completedLinesCount = 0;

	while (1)
	{
		GetBlock(fin, fout1, fout2, M, N, row, column, LinesLength, CompletedLines, &completedLinesCount, linesCount, INDEXES, flags);

		if (completedLinesCount != Min((linesCount - 1), M))
		{
			column++;
			t = 0;
			for (unsigned k = 0; k < M; k++) { // moving to the end of line going behind the first line of the next block
				t -= (LinesLength[1 + row * M + k]);
				t -= 2;
				if ((row * M + (k + 1) + 1) == linesCount) break;
			}
			fin->seekg(t, ios::cur);
		}
		else break;
	}

	DeleteINDEXES(INDEXES, M);
	delete[] CompletedLines;
	delete[] flags;
	return 0;
}

void OutResult(fstream* fin, fstream* fout, streampos** INDEXES, unsigned M, unsigned N, unsigned row, unsigned j, bool flag) {
	char s;
	streampos pos;
	pos = fin->tellg();

	*fout << "\nРезультат для " << row * M + (j + 1) << " строки:\n";
	*fout << "\tИмя первого массива: ";
	fin->seekg(INDEXES[j][2], ios::beg);
	for (int i = 0; i < (INDEXES[j][3] - INDEXES[j][2]); i++) {
		*fin >> s; *fout << s;
	};
	if (INDEXES[j][5] == -1) *fout << "\n\tМассив одномерный\n";
	else *fout << "\n\tМассив не одномерный\n";

	if (flag)
	{
		fin->seekg(INDEXES[j][8], ios::beg);
		*fout << "\tИмя второго массива: ";
		for (int i = 0; i < (INDEXES[j][9] - INDEXES[j][8]); i++) {
			*fin >> s; *fout << s;
		}
		if (INDEXES[j][11] == -1) *fout << "\n\tМассив одномерный\n";
		else *fout << "\n\tМассив не одномерный\n";
	}

	fin->seekg(pos, ios::beg);
}

int Process(struct Block block, unsigned* LinesLength, unsigned linesCount)
{
	fstream fin, fout1, fout2;
	unsigned row, column, rowsCount; // row - ряд блока, column - столбец блока

	fout1.open("out1.txt", ios::out);
	fout2.open("out2.txt", ios::out);
	fin.open("in.txt", ios::in);
	if (!fin.is_open()) { OutError(&fout1, 11); fin.close(); fout2.close(); return 0; }

	fout1 << "Фролов Александр 2302.\n\n"; fout2 << "Фролов Александр 2302.\n\n";
	fin << resetiosflags(ios::skipws);
	fin.seekg(LinesLength[0], ios::beg);

	row = 0; column = 0;
	rowsCount = GetRowsCount(linesCount, block.M);

	// считывание всех данных из файла (кроме первой строки) блоками
	while (1)
	{
		GetRowOfBlocks(&fin, &fout1, &fout2, block.M, block.str.N, row, column, LinesLength, linesCount);
		row++; column = 0;
		if (row == rowsCount) break;
	}

	fin.close(); fout1.close(); fout2.close();
	return 0;
}