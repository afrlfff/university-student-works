/* Задание #17. Лабораторная работа #4.
*  Автор: Фролов Александр Эдуардович
*  Группа: 2302
*  Версия: 1.1
*/

#include <iostream>
#include <fstream>
using namespace std;

void main(void)
{
	setlocale(LC_CTYPE, "rus"); // русский язык в консоли
	const unsigned N = 15;
	float A[N], B[N], C[N];
	int L, i, ind_B, ind_C;
	fstream f;
	cout << "Автор: Фролов Александр Эдуардович \n\n";
	f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_1/in.txt", ios::in);

	if (!f.is_open()) cout << "Проблемы с открытием файла :(\n";
	else {
		f >> L;
		if (f.eof()) {
			cout << "В исходном файле недостаточно данных\n"; // дано <2 значений
			f << "В исходном файле недостаточно данных\n"; // дано <2 значений
		} else {
			if (L < 0) L = 0;
			i = 0;
			while (i < L) {
				f >> A[i];
				i++;
				if ((f.eof()) || (i >= N)) { L = i; break; }
			}
			f.close(); f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_1/out.txt", ios::out);
			f << "Автор: Фролов Александр Эдуардович \n\n";

			cout << "Всего элементов в исходном массиве = " << L << endl;
			f << "Всего элементов в исходном массиве = " << L << endl;

			cout << "Исходный массив А: [";
			f << "Исходный массив А: [";
			for (i = 0; i < L; i++) {
				cout << A[i]; f << A[i];
				if (i != (L - 1)) {
					cout << ", "; f << ", ";
				}
			}
			cout << "]" << endl; f << "]" << endl;
			
			ind_B = 0;
			for (i = 0; i < L; i++) {
				// заполняю массив B всеми положительными числами массива А
				if (A[i] > 0) {
					B[ind_B] = A[i];
					ind_B++;
				}
			} for (i = ind_B; i < L; i++) {
				// заполняю лишние элементы массива B отрицательными числами
				B[i] = -1;
			}
			ind_C = 0;
			for (i = (L-1); i >= 0; i--) {
				// заполняю массив С всеми отрицательными числами массива А
				if (A[i] < 0) {
					C[ind_C] = A[i];
					ind_C++;
				}
			} for (i = ind_C; i < L; i++) {
				// заполняю лишние элементы массива С положителньыми числами
				C[i] = 1;
			}
			
			cout << "Массив В: [";
			f << "Массив В: [";
			for (i = 0; i < L; i++) {
				// вывожу все положительные числа массива В
				if (B[i] < 0) break;
				else {
					cout << B[i]; f << B[i];
					if (i != (ind_B - 1)) {
						cout << ", "; f << ", ";
					}
				}
			}
			cout << "]" << endl << "Массив C: [";
			f << "]" << endl << "Массив C: [";
			for (i = 0; i < L; i++) {
				// вывожу все отрацательные числа массива С
				if (C[i] > 0) break;
				else {
					cout << C[i]; f << C[i];
					if (i != (ind_C - 1)) {
						cout << ", "; f << ", ";
					}
				}
			}
			cout << "]" << endl; f << "]" << endl;
		}
		f.close();
	}
}