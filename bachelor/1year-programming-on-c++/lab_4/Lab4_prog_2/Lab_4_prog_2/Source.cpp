/* Задание #17. Лабораторная работа #4.
*  Автор: Фролов Александр Эдуардович
*  Группа: 2302
*  Версия: 2.1
*/

#include <iostream>
#include <fstream>
using namespace std;

int main()
{
	setlocale(LC_CTYPE, "rus"); // русский язык в консоли
	float *A, *B, *C, tmp;
	float *p, *q;
	int L, i, kp, ko;
	fstream f;
	cout << "Автор: Фролов Александр Эдуардович \n\n";
	f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_2/in.txt", ios::in);

	if (!f.is_open()) cout << "Проблемы с открытием файла :(\n";
	else {
		if (!f.eof()) {
			L = 0;
			while ((f >> tmp) && (L < 15)) L++;
		}
		A = new float[L+1];
		if (A == NULL) {
			cout << "Проблемы с выделением памяти для массива A. \n";
			f << "Проблемы с выделением памяти для массива A. \n";
			return 0;
		}

		f.close(); f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_2/in.txt", ios::in);
		kp = 0; ko = 0;
		for (p = A; p != (A + L); p++) {
			f >> tmp;
			*p = tmp;
			if (*p > 0) kp++;
			else if (*p < 0) ko++;
		}
		f.close(); f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_2/out.txt", ios::out);
		f << "Автор: Фролов Александр Эдуардович \n\n";

		cout << "Всего элементов в исходном массиве = " << L << endl;
		f << "Всего элементов в исходном массиве = " << L << endl;

		cout << "Исходный массив А: [";
		f << "Исходный массив А: [";
		for (p = A; p != A + L; p++) {
			cout << *p; f << *p;
			if ((p-A) != (L - 1)) {
				cout << ", "; f << ", ";
			}
		}
		cout << "]" << endl; f << "]" << endl;

		B = new float[kp];
		if (B == NULL) {
			cout << "Проблемы с выделением памяти для массива B. \n";
			f << "Проблемы с выделением памяти для массива B. \n";
			return 0;
		}
		for (p = A, q = B; p != A + L; p++) {
			// заполняю массив B всеми положительными числами массива А
			if (*p > 0) {
				*q = *p;
				q++;
			}
		}
		cout << "Массив В: ["; f << "Массив В: [";
		for (p = B; p != (B + kp); p++) {
			cout << *p; f << *p;
			if (p != (B + kp - 1)) {
				cout << ", "; f << ", ";
			}
		}
		cout << "]" << endl; f << "]" << endl;

		C = new float[ko];
		if (C == NULL) {
			cout << "Проблемы с выделением памяти для массива C. \n";
			f << "Проблемы с выделением памяти для массива C. \n";
			return 0;
		}
		for (p = A+L-1, q = C; p != A-1; p--) {
			// заполняю массив C всеми отрицательными числами массива А
			if (*p < 0) {
				*q = *p;
				q++;
			}
		}
		cout << "Массив C: ["; f << "Массив C: [";
		for (p = C; p != C + ko; p++) {
			cout << *p; f << *p;
			if (p != (C + ko - 1)) {
				cout << ", "; f << ", ";
			}
		}
		cout << "]" << endl; f << "]" << endl;
		delete[] A;
		delete[] B;
		delete[] C;
		f.close();
	}
}