#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;

class StrL {
	char* pStroka;
	unsigned L;
public:
	void set_pStroka() {
		cout << "Память выделена. \n";
		pStroka = new char[L];
	}
	void set_L(unsigned k) {
		L = k;
	}

	// вспомогательная функция
	void GetBeginOfStr(fstream* f, int k, bool isEnd) {
		if (isEnd) {
			f->close(); f->open("in4.txt", ios::in);
			f->seekg(-k, ios::end);
		}
		else f->seekg(-k, ios::cur);
	}
	// вспомогательная функция
	bool GetStopNumber(fstream* fin, fstream* fout, int* stopNumber) {
		char s;

		while (1) { // считвание числа-ограничителя
			(*fin) >> s;
			if ((*fin).eof()) {
				(*fout) << "Ошибка: в файле in4.txt должны быть хотя бы 2 непустые строки\n";
				return false;
			}
			else if (s == '\n') {
				(*fout) << "Ошибка: не удалось считать число-ограничитель.\n";
				return false;
			}
			else if (s == '0' || s == '1' || s == '2' || s == '3' || s == '4' || s == '5'
				|| s == '6' || s == '7' || s == '8' || s == '9')
			{
				(*fin).unget(); (*fin) >> (*stopNumber);
				return true;
			}
		}
		return false;
	}

	bool GetStr(fstream* fin, fstream* fout) {
		char s; // переменная для считвания символов
		int stopNumber; // символ-ограничитель из первой строки первого файла
		int k; // k - кол-во всех считанных символов в строке (до конца файла или стоп-символа);
		bool isEnd = false; // тк если будет конец файла, то seekg() не будет работать

		if (!(*fin).is_open()) {
			(*fout) << "Ошибка: проблемы с открытием файла in4.txt.\n";
			return true;
		}

		(*fin) << resetiosflags(ios::skipws);

		if (!(GetStopNumber(fin, fout, &stopNumber))) {
			return true;
		}

		do {
			if ((*fin).eof()) {
				(*fout) << "Ошибка: в файле in4.txt должны быть хотя бы 2 непустые строки\n";
				return true;
			}
			(*fin) >> s;
		} while (s != '\n');

		// Пройдусь по второй строке, чтобы посчитать количество символов
		k = 0; s = ' ';
		while (!(k == stopNumber || s == '\n')) {
			(*fin) >> s;
			if ((*fin).eof()) {
				isEnd = true;
				break;
			}
			k++;
		}

		set_L(k);
		set_pStroka();

		// Возврат в начало последней строки файла
		GetBeginOfStr(fin, k, isEnd);

		// Заполнение массива pStroka исходной строкой
		for (int i = 0; i < k; i++) {
			(*fin) >> s; pStroka[i] = s;
		}

		// Возврат в начало последней строки файла для корректной работы след. функций
		GetBeginOfStr(fin, k, isEnd);

		return false;
	}

	void Solving() {
		int i;
		unsigned count = 0; // количество точек в строке
		char* pStroka2 = new char[L];

		for (unsigned j = 0; j < L; j++) {
			pStroka2[j] = pStroka[j];
			if (pStroka[j] == '.') count++;
		}
		i = L - 1; // индекс последнего символа в исходной строке

		set_L(L + count * 2);
		delete[] pStroka; cout << "Память освобождена. \n";
		set_pStroka();

		while (i >= 0) {
			if (pStroka2[i] == '.') {
				pStroka[i + count * 2] = '.';
				pStroka[i + count * 2 - 1] = '.';
				pStroka[i + count * 2 - 2] = '.';
				count--;
			}
			else {
				pStroka[i + count * 2] = pStroka2[i];
			}
			i--;
		}
		delete[] pStroka2;
	}

	void Out(fstream* fout) {
		for (unsigned i = 0; i < L; i++) {
			(*fout) << pStroka[i];
		}
		(*fout) << endl;
	}

	~StrL()
	{
		if (pStroka != NULL) delete[] pStroka;
		cout << "Память освобождена. \n";
	}

};

int main() {
	setlocale(LC_ALL, "rus");

	fstream fin, fout;
	StrL stroka;

	fin.open("in4.txt", ios::in);
	fout.open("out4.txt", ios::out);
	fout << "Фролов Александр 2302\n\n";

	if (!(stroka.GetStr(&fin, &fout))) {
		fout << "Решение для файла in4.txt:\n\nНачальная строка: \t";
		stroka.Out(&fout);
		stroka.Solving();
		fout << "Новая строка: \t\t";
		stroka.Out(&fout);
	}

	fin.close();
	fout.close();
	return 0;
}