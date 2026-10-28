#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>

using namespace std;

const unsigned N = 100;

void OutIncorrectLines(int k0, int k1, int k2, fstream &fprotok) {
	int K[3] = { k0, k1, k2 };
	string S[3];
	int k;
	for (int i = 0; i < 3; i++) {
		k = K[i];
		if (k%10 == 1) S[i] = "а";
		if (k%10 == 2 || k%10 == 3 || k%10 == 4) S[i] = "и";
		else S[i] = "";
	}
	
	fprotok << "3) В результате считывания входного файла было замечено:\n"
		<< "\t" << k0 << " строк" << S[0] << " без чисел - строки игнорируются программой.\n"
		<< "\t" << k1 << " строк" << S[1] << " без координаты y - строки игнорируются программой.\n"
		<< "\t" << k2 << " строк" << S[2] << " с 2-мя и более числами - лишние числа отброшены.\n";
}
bool CheckErrors(fstream &fin, fstream &frez, fstream &fprotok, const unsigned N, int *kmax) {
	char s; float tmp;
	int n; // кол-во точек (первое число в файле)
	bool correctFirstLine = true;
	
	fin << resetiosflags(ios::skipws);
	fprotok << "ПРОТОКОЛ К КУРСОВОЙ РАБОТЕ.\n\nШАГ 1. Считывание данных из входного файла.\n\n";

	if (!fin.is_open() || !frez.is_open() || !fprotok.is_open()) { fprotok << "ОШИБКА: Проблемы с открытием файла.\n"; return true; }
	do {fin >> s; if (fin.eof()) { fprotok << "ОШИБКА: В файле нет чисел."; return true; }} while (s == ' ');
	if (s == '\n') { fprotok << "ОШИБКА: В первой строке файла не указано число точек.\n"; return true; }
	else { fin.unget(); fin >> n; }
	if (n < 1) { fprotok << "ОШИБКА: Число точек не может быть меньше 1.\n"; return true; }
	if (n > N) { fprotok << "ОШИБКА: Число точек не может быть больше 100.\n"; return true; }
	do { fin >> s; if (fin.eof()) { fprotok << "ОШИБКА: В файле нет чисел."; return true; } if (s != ' ') { correctFirstLine = false; }} while (s != '\n');
	if (!correctFirstLine) fprotok << "0) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: в первой строке дано больше одного числа (было считано только первое).\n";
	fprotok << "1) Заданное вами количество точек(число в первой строке): n = " << n << ".\n";

	bool goodPoint = false; // // true - хотя бы одна корректно указанная точка
	int k = 0; // кол-во считанных строк
	int k0 = 0, k1 = 0, k2 = 0; // кол-во пустых строк, кол-во строк с 1-м числом, кол-во строк с >=2 числами
	while (true) {
		if (k == N) break;
		do {
			fin >> s;
			if (fin.eof()) {
				if (!goodPoint) { fprotok << "2) ОШИБКА: В файле нет ни одной корректно указанной точки.\n"; return true; }
				k0++;
				if (k < n) {
					fprotok << "2) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: число корректно заданных точек меньше, чем n.\n" 
						<< "(из файла были считаны все корректно заданные точки)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else if (k > n) {
					fprotok << "2) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: число корректно заданных точек больше, чем n.\n"
						<< "(из файла были считаны первые n корректно заданных точек)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				if (k2 >= n) *kmax = n;
				else *kmax = k2;
				return false;
			}
		} while (s == ' ');
		if (s == '\n') { continue; }
		else { fin.unget(); fin >> tmp; }
		do {
			fin >> s;
			if (fin.eof()) {
				k1++;
				if (!goodPoint) { fprotok << "2) ОШИБКА: В файле нет ни одной корректно указанной точки.\n"; return true; }
				else if (k < n) {
					fprotok << "2) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: число корректно заданных точек меньше, чем n.\n"
						<< "(из файла были считаны все корректно заданные точки)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else if (k > n) {
					fprotok << "2) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: число корректно заданных точек больше, чем n.\n"
						<< "(из файла были считаны первые n корректно заданных точек)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				if (k2 >= n) *kmax = n;
				else *kmax = k2;
				return false;
			}
		} while (s == ' ');
		if (s == '\n') { continue; }
		else { fin.unget(); fin >> tmp; goodPoint = true; k++; k2++; }
		do {
			fin >> s;
			if (fin.eof()) {
				if (k < n) {
					fprotok << "2) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: число корректно заданных точек меньше, чем n.\n"
						<< "(из файла были считаны все корректно заданные точки)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else if (k > n) {
					fprotok << "2) НЕЗНАЧИТЕЛЬНАЯ ОШИБКА: число корректно заданных точек больше, чем n.\n" 
						<< "(из файла были считаны первые n корректно заданных точек)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else fprotok << "2) Во входном файле нет ни одной ошибки.\n";
				if (k2 >= n) *kmax = n;
				else *kmax = k2;
				return false;
			}
		} while (s != '\n');
	}
	
	OutIncorrectLines(k0, k1, k2, fprotok);
	if (k2 >= n) *kmax = n;
	else *kmax = k2;
	return false;
}
int GetPoints(fstream& fin, float POINTS[N][2], int *kmax) {
	char s;
	int n; // кол-во точек (первое число в файле)
	float x, y; // элементы массива
	int k = 0; // кол-во считанных строк

	fin << resetiosflags(ios::skipws);
	fin >> n;
	do { fin >> s; } while (s != '\n');

	while (true) {
		if (k == N) break;
		do { fin >> s; if (fin.eof()) return k; } while (s == ' ');
		if (s == '\n') continue;
		else { fin.unget(); fin >> x; }
		do { fin >> s; if (fin.eof()) return k; } while (s == ' ');
		if (s == '\n') continue;
		else {
			fin.unget(); fin >> y;
			POINTS[k][0] = x; POINTS[k][1] = y;
			k++;
			if (k == *kmax) break;
		} do { fin >> s; if (fin.eof()) return k; } while (s == ' ');
	}
	return k;
}
int OutPoints(float POINTS[N][2], int n, fstream& fprotok) {
	if (n%10 == 1) fprotok << "\nШАГ 2. Считана " << n << " точка со следующими координами:\n";
	else if (n % 10 == 2 || n % 10 == 3 || n % 10 == 4) fprotok << "\nШАГ 2. Считано " << n << " точки со следующими координами:\n";
	else fprotok << "\nШАГ 2. Считано " << n << " точек со следующими координами:\n";
	
	for (int i = 0; i < n; i++) {
		fprotok << "\t(" << POINTS[i][0] << ";" << POINTS[i][1] << ")";
		if (i == n - 1) fprotok << ".\n";
		else fprotok << ",\n";
	}
	fprotok << endl; return 0;
}
int TaskSolving(float POINTS[N][2], int n, fstream& fprotok, fstream& frez) {
	float x1, y1, x2, y2, x3, y3;
	float r12, r13, r23;
	float R[3];
	float kat1, kat2, gip;
	float eps = 1e-3; // для сравнения дробных чисел
	bool isRightTriangle = false; // если данный треугольник прямоугольный
	float kx; // для составления уравнения прямой
	unsigned ind = 1, ind2 = 1;

	fprotok << "ШАГ 3. Решение поставленной задачи.\n\n";
	if (n < 3) {
		fprotok << "По заданным точкам не удалось построить ни одного прямоугольного треугольника.";
		frez << "По заданным точкам не удалось построить ни одного прямоугольного треугольника.";
		return 0;
	}

	for (int i = 0; i < n-2; i++) {
		for (int j = i+1; j < n-1; j++) {
			for (int k = j + 1; k < n; k++) {
				x1 = POINTS[i][0]; y1 = POINTS[i][1];
				x2 = POINTS[j][0]; y2 = POINTS[j][1];
				x3 = POINTS[k][0]; y3 = POINTS[k][1];
				
				fprotok << ind << ") Рассмотрим треугольник с точками A(" << x1 << ";" << y1 << "), B("
					<< x2 << ";" << y2 << "), C(" << x3 << ";" << y3 << ").\n";
				ind++;
				if ((x1 == x2 && y1 == y2)|| (x2 == x3 && y2 == y3)|| (x1 == x3 && y1 == y3)) {
					fprotok << "\tТреугольник невозможно составить, т.к. имеются одинаковые точки.\n\n";
					continue;
				} else {
					kx = abs(y2-y1) / abs(x2 - x1); // угловой коэффициент
					// уравнение прямой: y - y0 = k(x - x0) ---> y = k(x - x0) + y0
					// при х0 = х1 мы составляем уравнение прямой, проходящей через первые 2 точки
					// это уравнение: y = k(x - x1) + y1, где k = y2/y1
					if (abs(y3 - (kx * (x3 - x1) + y1)) < eps) { // если и 3-я точка лежит на прямой (y3 == kx(x3 - x1) + y1)
						fprotok << "\tТреугольник невозможно составить, т.к. все три точки лежат на одной прямой.\n\n";
						continue;
					}
				}
				r12 = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
				r13 = sqrt((x3 - x1) * (x3 - x1) + (y3 - y1) * (y3 - y1));
				r23 = sqrt((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2));
				R[0] = r12; R[1] = r13; R[2] = r23;
				fprotok << "\tТочки не равны между собой и не лежат на одной прямой, поэтому применим теорему Пифагора:\n"
					<< "\tПо формуле расстояния между точками, AB = " << r12 << ", BC = " << r23 << ", AC = " << r13 << ".\n";

				for (int l = 0; l < 3; l++) {
					gip = R[l]; kat1 = R[(l + 1) % 3]; kat2 = R[(l + 2) % 3];
					if (abs(gip * gip - (kat1 * kat1 + kat2 * kat2)) < eps) {
						isRightTriangle = true;
						break;
					}
				}
				if (isRightTriangle) {
					fprotok << "\tПо теореме Пифагора данный треугольник - ПРЯМОУГОЛЬНЫЙ\n\n";
					frez << ind2 << ") треугольник с точками (" << x1 << "; " << y1 << "), ("
						<< x2 << ";" << y2 << "), (" << x3 << ";" << y3 << ") --- прямоугольный\n";
					ind2++;
					isRightTriangle = false;
				} else {
					fprotok << "\tПо теореме Пифагора данный треугольник - НЕ ПРЯМОУГОЛЬНЫЙ\n\n";
				}
			}
		}
	}
	if (ind2 == 1) {
		fprotok << "По заданным точкам не удалось построить ни одного прямоугольного треугольника.";
		frez << "По заданным точкам не удалось построить ни одного прямоугольного треугольника.";
		return 0;
	}
}

int main() {
	bool isErrors;
	fstream fin, frez, fprotok;
	float POINTS[N][2];
	int n; // кол-во точек
	int *kmax = new int; // макс. кол-во точек, которые можно считать из файла

	setlocale(LC_ALL, "rus");

	fin.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/points.txt", ios::in);
	frez.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/result.txt", ios::out);
	fprotok.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/protokol.txt", ios::out);
	isErrors = CheckErrors(fin, frez, fprotok, N, kmax); // true - есть ошибки, false - нету
	// также CheckErrors() записывает значение в kmax

	if (isErrors) {
		fprotok << "(т.к. во входном файле обнаружены ошибки, дальнейшая работа программы невозможна)";
		frez << "Т.к. во входном файле обнаружены ошибки, дальнейшая работа программы невозможна.";
		return 0;
	}
	else {
		fin.close(); fin.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/points.txt", ios::in);
		n = GetPoints(fin, POINTS, kmax); // заполняет массив POINTS заданными точками и возвращает кол-во точек
		OutPoints(POINTS, n, fprotok); // выводит все считанные точки в файл протокола
		TaskSolving(POINTS, n, fprotok, frez); // решение поставленной задачи
	}
	fin.close(); frez.close(); fprotok.close();
}