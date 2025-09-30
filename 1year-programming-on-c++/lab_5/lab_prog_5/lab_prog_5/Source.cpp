/* Задание #20(н). Лабораторная работа #5.
*  Автор: Фролов Александр Эдуардович
*  Группа: 2302
*  Версия: 1.1
*/

#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;

const int N = 10; // макс размер массива А

bool CheckErrors(const int N, fstream &f) {
	char s; int r; int m; // r - размер матрицы из файла(тк переменная N занята)

	f << resetiosflags(ios::skipws);

	if (!f.is_open()) { cout << "Проблемы с открытием файла. \n"; return false; }
	do { f >> s; } while (s == ' ');
	if (s == '\n') { cout << "В файле не указан размер матрицы N \n"; return false; }
	else { f.unget(); f >> r; }
	do { f >> s; } while (s == ' ');
	if (s == '\n') { cout << "В файле не указано число m \n"; return false; }
	else { f.unget(); f >> m; }
	if (r > N) { cout << "Задан слишком большой размер матрицы \n"; return false; }
	else if (r <= 0) { cout << "Задан слишком маленький размер матрицы. \n"; return false; }
	else if (m <= 0) { cout << "число r не может быть меньше 1 \n"; return false; }
	int r2;
	if (r % 2 == 0) r2 = r / 2;
	else r2 = r / 2 + 1;
	if (m > r2) { cout << "число m не может больше, чем N/2 \n"; return false; }
	while (s != '\n') f >> s;

	return true;
}
pair<int, int> StartSizeArr(fstream &f) {
	char s; int r; int m; // r - размер матрицы из файла
	f << resetiosflags(ios::skipws);

	do { f >> s; } while (s == ' ');
	f.unget(); f >> r;
	do { f >> s; } while (s == ' ');
	f.unget(); f >> m;
	while (s != '\n') f >> s;
	return pair<int, int>(r, m);
}
int OutStartArr(const int N, fstream &f1, fstream& f2) {
	char s;
	float tmp;

	f2 << resetiosflags(ios::skipws);
	do { f1 >> s; } while (s != '\n');

	while (1) {
		f1 >> s;
		if (f1.eof()) { cout << "\n\n"; f2 << "\n\n"; return 0; }
		else if ((s == ' ') || (s == '\n')) {
			if (s == '\n') { cout << s; f2 << s; }
			else {
				while (s == ' ') {
					f1 >> s;
					if (f1.eof()) { cout << "\n\n"; f2 << "\n\n"; return 0; }
				}
				if (s == '\n') { cout << s; f2 << s; }
				else {
					f1.unget(); f1 >> tmp;
					cout << tmp << " ";
					f2 << tmp << " ";
				}
			}
		} else {
			f1.unget(); f1 >> tmp;
			cout << tmp << " ";
			f2 << tmp << " ";
		}
	}
	cout << "\n\n"; f2 << "\n\n"; return 0;
}
int NewSizeArr(const int N, int r, fstream &f) {
	unsigned size_el, size_str; // считают кол-во элеметов в строке и количество строк
	char s;
	float tmp;

	f << resetiosflags(ios::skipws);
	do { f >> s; } while (s != '\n');

	size_el = 0; size_str = 1;
	while (1) {
		f >> s;
		if (f.eof()) {
			if (size_el < r) r = size_el;
			if (size_str < r) r = size_str;
			return r;
		} else if ((s == ' ') || (s == '\n')) {
			if (s == '\n') {
				if (size_el < r) r = size_el;
				size_el = 0; size_str++;
			}
			else {
				while (s == ' ') {
					f >> s;
					if (f.eof()) {
						if (size_str < r) r = size_str;
						return r;
					}
				}
				if (s == '\n') { size_el = 0; size_str++; }
				else { f.unget(); f >> tmp; size_el++; }
			}
		} else { f.unget(); f >> tmp; size_el++; }
	}
	if (size_str < r) r = size_str;
	return r;
}

int InpArr(float A[N][N], unsigned n, fstream& f) {
	int r; char s, i, j;
	float tmp;
	bool skip = false;

	do { f >> s; } while (s != '\n');

	i = 0; j = 0;
	while (1) {
		f >> s;
		if (f.eof()) return 0;
		else if ((s == ' ') || (s == '\n')) {
			if (s == '\n'){ skip = false; i++; j = 0; }
			else {
				while (s == ' ') {
					f >> s;
					if (f.eof()) return 0;
				}
				if (s == '\n') { skip = false; i++; j = 0; }
				else {
					if (!skip) {
						f.unget(); f >> tmp;
						A[i][j] = tmp; j++;
					}
					if (j == n) skip = true;
				}
			}
		} else {
			if (!skip) {
				f.unget(); f >> tmp;
				A[i][j] = tmp; j++;
			}
			if (j == n) skip = true;
		}
	}
	return 0;
}
void OutArr(float A[N][N], unsigned n, fstream &f) {
	cout << "Новая матрица: " << "N = " << n << endl;
	f << "Новая матрица: " << "N = " << n << endl;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			cout << A[i][j] << " ";
			f << A[i][j] << " ";
		}
		cout << endl; f << endl;
	}
	cout << endl; f << endl;
}
float TaskSolve(float A[N][N], int m, unsigned n, float maxEl, fstream &f) {
	unsigned n2, k;
	float el;

	cout << "Решение задачи для N = " << n << " и m = " << m << ".\n";
	f << "Решение задачи для N = " << n << " и m = " << m << ".\n";
	cout << "Задействованные элементы: \n";
	if (n % 2 == 0) n2 = n / 2;
	else n2 = n / 2 + 1;
	for (int i = (m-1); i < n2; i++) {
		if (i == (m - 1)) {
			el = A[i][m - 1];
			cout << el << " ";
			if (el > maxEl) maxEl = el;
			el = A[i][n2 - 1];
			cout << el << " ";
			if (el > maxEl) maxEl = el;
		}
		else if ( (i < (n2 - 1)) && (i > (m-1))) {
			for (int j = m; j < n2; j++) {
				el = A[i][j];
				cout << el << " ";
				if (el > maxEl) maxEl = el;
			}
		}
		else if (i == (n2 - 1)) {
			for (int j = (m - 1); j < n2; j++) {
				el = A[i][j];
				cout << el << " ";
				if (el > maxEl) maxEl = el;
			}
		}
		cout << endl;
	}
	k = n2 + 1;
	for (int i = n2; i < n; i++) {
		el = A[i][k-1];
		cout << el << " ";
		if (el > maxEl) maxEl = el;
		k++;
	}
	cout << "\nМаксимальный элемент в заштрихованной области: " << maxEl << endl;
	f << "\nМаксимальный элемент в заштрихованной области: " << maxEl << endl;
	return maxEl;
}
void main(void)
{
	setlocale(LC_CTYPE, "rus"); // русский язык в консоли
	float A[N][N], maxEl = -10000;
	fstream f1, f2;
	int r, m; // r, m - числа первой строка файла числа
	unsigned n, n2;
	bool isWork = true;
	
	f1.open("C:/Users/DNS/Desktop/c++/lab_5/in.txt", ios::in);
	isWork = CheckErrors(N, f1);

	if (isWork) {
		f1.close(); f1.open("C:/Users/DNS/Desktop/c++/lab_5/in.txt", ios::in);
		r = StartSizeArr(f1).first;
		f1.close(); f1.open("C:/Users/DNS/Desktop/c++/lab_5/in.txt", ios::in);
		m = StartSizeArr(f1).second;

		f1.close(); f1.open("C:/Users/DNS/Desktop/c++/lab_5/in.txt", ios::in);
		f2.open("C:/Users/DNS/Desktop/c++/lab_5/out.txt", ios::out);
		cout << "Автор: Фролов Александр Эдуардович.\nГруппа 2302. \nНачальная матрица:\n";
		f2 << "Автор: Фролов Александр Эдуардович.\nГруппа 2302. \nНачальная матрица:\n";
		OutStartArr(N, f1, f2);

		f1.close(); f1.open("C:/Users/DNS/Desktop/c++/lab_5/in.txt", ios::in);
		n = NewSizeArr(N, r, f1);

		if (n % 2 == 0) n2 = n / 2;
		else n2 = n / 2 + 1;
		if (m <= n2) {
			f1.close(); f1.open("C:/Users/DNS/Desktop/c++/lab_5/in.txt", ios::in);
			InpArr(A, n, f1); // преобразовывает матрицу А, запонляя n*n элементов
			OutArr(A, n, f2); // выводит матрицу А в файл
			TaskSolve(A, m, n, maxEl, f2); // решение задачи и вывод результата
		} else cout << "Значение m меньше нового размера матрицы N \n";
		f1.close(); f2.close();
	}
	f1.close();
}