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
		if (k%10 == 1) S[i] = "�";
		if (k%10 == 2 || k%10 == 3 || k%10 == 4) S[i] = "�";
		else S[i] = "";
	}
	
	fprotok << "3) � ���������� ���������� �������� ����� ���� ��������:\n"
		<< "\t" << k0 << " �����" << S[0] << " ��� ����� - ������ ������������ ����������.\n"
		<< "\t" << k1 << " �����" << S[1] << " ��� ���������� y - ������ ������������ ����������.\n"
		<< "\t" << k2 << " �����" << S[2] << " � 2-�� � ����� ������� - ������ ����� ���������.\n";
}
bool CheckErrors(fstream &fin, fstream &frez, fstream &fprotok, const unsigned N, int *kmax) {
	char s; float tmp;
	int n; // ���-�� ����� (������ ����� � �����)
	bool correctFirstLine = true;
	
	fin << resetiosflags(ios::skipws);
	fprotok << "�������� � �������� ������.\n\n��� 1. ���������� ������ �� �������� �����.\n\n";

	if (!fin.is_open() || !frez.is_open() || !fprotok.is_open()) { fprotok << "������: �������� � ��������� �����.\n"; return true; }
	do {fin >> s; if (fin.eof()) { fprotok << "������: � ����� ��� �����."; return true; }} while (s == ' ');
	if (s == '\n') { fprotok << "������: � ������ ������ ����� �� ������� ����� �����.\n"; return true; }
	else { fin.unget(); fin >> n; }
	if (n < 1) { fprotok << "������: ����� ����� �� ����� ���� ������ 1.\n"; return true; }
	if (n > N) { fprotok << "������: ����� ����� �� ����� ���� ������ 100.\n"; return true; }
	do { fin >> s; if (fin.eof()) { fprotok << "������: � ����� ��� �����."; return true; } if (s != ' ') { correctFirstLine = false; }} while (s != '\n');
	if (!correctFirstLine) fprotok << "0) �������������� ������: � ������ ������ ���� ������ ������ ����� (���� ������� ������ ������).\n";
	fprotok << "1) �������� ���� ���������� �����(����� � ������ ������): n = " << n << ".\n";

	bool goodPoint = false; // // true - ���� �� ���� ��������� ��������� �����
	int k = 0; // ���-�� ��������� �����
	int k0 = 0, k1 = 0, k2 = 0; // ���-�� ������ �����, ���-�� ����� � 1-� ������, ���-�� ����� � >=2 �������
	while (true) {
		if (k == N) break;
		do {
			fin >> s;
			if (fin.eof()) {
				if (!goodPoint) { fprotok << "2) ������: � ����� ��� �� ����� ��������� ��������� �����.\n"; return true; }
				k0++;
				if (k < n) {
					fprotok << "2) �������������� ������: ����� ��������� �������� ����� ������, ��� n.\n" 
						<< "(�� ����� ���� ������� ��� ��������� �������� �����)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else if (k > n) {
					fprotok << "2) �������������� ������: ����� ��������� �������� ����� ������, ��� n.\n"
						<< "(�� ����� ���� ������� ������ n ��������� �������� �����)\n";
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
				if (!goodPoint) { fprotok << "2) ������: � ����� ��� �� ����� ��������� ��������� �����.\n"; return true; }
				else if (k < n) {
					fprotok << "2) �������������� ������: ����� ��������� �������� ����� ������, ��� n.\n"
						<< "(�� ����� ���� ������� ��� ��������� �������� �����)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else if (k > n) {
					fprotok << "2) �������������� ������: ����� ��������� �������� ����� ������, ��� n.\n"
						<< "(�� ����� ���� ������� ������ n ��������� �������� �����)\n";
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
					fprotok << "2) �������������� ������: ����� ��������� �������� ����� ������, ��� n.\n"
						<< "(�� ����� ���� ������� ��� ��������� �������� �����)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else if (k > n) {
					fprotok << "2) �������������� ������: ����� ��������� �������� ����� ������, ��� n.\n" 
						<< "(�� ����� ���� ������� ������ n ��������� �������� �����)\n";
					OutIncorrectLines(k0, k1, k2, fprotok);
				}
				else fprotok << "2) �� ������� ����� ��� �� ����� ������.\n";
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
	int n; // ���-�� ����� (������ ����� � �����)
	float x, y; // �������� �������
	int k = 0; // ���-�� ��������� �����

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
	if (n%10 == 1) fprotok << "\n��� 2. ������� " << n << " ����� �� ���������� ����������:\n";
	else if (n % 10 == 2 || n % 10 == 3 || n % 10 == 4) fprotok << "\n��� 2. ������� " << n << " ����� �� ���������� ����������:\n";
	else fprotok << "\n��� 2. ������� " << n << " ����� �� ���������� ����������:\n";
	
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
	float eps = 1e-3; // ��� ��������� ������� �����
	bool isRightTriangle = false; // ���� ������ ����������� �������������
	float kx; // ��� ����������� ��������� ������
	unsigned ind = 1, ind2 = 1;

	fprotok << "��� 3. ������� ������������ ������.\n\n";
	if (n < 3) {
		fprotok << "�� �������� ������ �� ������� ��������� �� ������ �������������� ������������.";
		frez << "�� �������� ������ �� ������� ��������� �� ������ �������������� ������������.";
		return 0;
	}

	for (int i = 0; i < n-2; i++) {
		for (int j = i+1; j < n-1; j++) {
			for (int k = j + 1; k < n; k++) {
				x1 = POINTS[i][0]; y1 = POINTS[i][1];
				x2 = POINTS[j][0]; y2 = POINTS[j][1];
				x3 = POINTS[k][0]; y3 = POINTS[k][1];
				
				fprotok << ind << ") ���������� ����������� � ������� A(" << x1 << ";" << y1 << "), B("
					<< x2 << ";" << y2 << "), C(" << x3 << ";" << y3 << ").\n";
				ind++;
				if ((x1 == x2 && y1 == y2)|| (x2 == x3 && y2 == y3)|| (x1 == x3 && y1 == y3)) {
					fprotok << "\t����������� ���������� ���������, �.�. ������� ���������� �����.\n\n";
					continue;
				} else {
					kx = abs(y2-y1) / abs(x2 - x1); // ������� �����������
					// ��������� ������: y - y0 = k(x - x0) ---> y = k(x - x0) + y0
					// ��� �0 = �1 �� ���������� ��������� ������, ���������� ����� ������ 2 �����
					// ��� ���������: y = k(x - x1) + y1, ��� k = y2/y1
					if (abs(y3 - (kx * (x3 - x1) + y1)) < eps) { // ���� � 3-� ����� ����� �� ������ (y3 == kx(x3 - x1) + y1)
						fprotok << "\t����������� ���������� ���������, �.�. ��� ��� ����� ����� �� ����� ������.\n\n";
						continue;
					}
				}
				r12 = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
				r13 = sqrt((x3 - x1) * (x3 - x1) + (y3 - y1) * (y3 - y1));
				r23 = sqrt((x3 - x2) * (x3 - x2) + (y3 - y2) * (y3 - y2));
				R[0] = r12; R[1] = r13; R[2] = r23;
				fprotok << "\t����� �� ����� ����� ����� � �� ����� �� ����� ������, ������� �������� ������� ��������:\n"
					<< "\t�� ������� ���������� ����� �������, AB = " << r12 << ", BC = " << r23 << ", AC = " << r13 << ".\n";

				for (int l = 0; l < 3; l++) {
					gip = R[l]; kat1 = R[(l + 1) % 3]; kat2 = R[(l + 2) % 3];
					if (abs(gip * gip - (kat1 * kat1 + kat2 * kat2)) < eps) {
						isRightTriangle = true;
						break;
					}
				}
				if (isRightTriangle) {
					fprotok << "\t�� ������� �������� ������ ����������� - �������������\n\n";
					frez << ind2 << ") ����������� � ������� (" << x1 << "; " << y1 << "), ("
						<< x2 << ";" << y2 << "), (" << x3 << ";" << y3 << ") --- �������������\n";
					ind2++;
					isRightTriangle = false;
				} else {
					fprotok << "\t�� ������� �������� ������ ����������� - �� �������������\n\n";
				}
			}
		}
	}
	if (ind2 == 1) {
		fprotok << "�� �������� ������ �� ������� ��������� �� ������ �������������� ������������.";
		frez << "�� �������� ������ �� ������� ��������� �� ������ �������������� ������������.";
		return 0;
	}
}

int main() {
	bool isErrors;
	fstream fin, frez, fprotok;
	float POINTS[N][2];
	int n; // ���-�� �����
	int *kmax = new int; // ����. ���-�� �����, ������� ����� ������� �� �����

	setlocale(LC_ALL, "rus");

	fin.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/points.txt", ios::in);
	frez.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/result.txt", ios::out);
	fprotok.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/protokol.txt", ios::out);
	isErrors = CheckErrors(fin, frez, fprotok, N, kmax); // true - ���� ������, false - ����
	// ����� CheckErrors() ���������� �������� � kmax

	if (isErrors) {
		fprotok << "(�.�. �� ������� ����� ���������� ������, ���������� ������ ��������� ����������)";
		frez << "�.�. �� ������� ����� ���������� ������, ���������� ������ ��������� ����������.";
		return 0;
	}
	else {
		fin.close(); fin.open("C:/Users/DNS/Desktop/c++/Kursovik_1sem/points.txt", ios::in);
		n = GetPoints(fin, POINTS, kmax); // ��������� ������ POINTS ��������� ������� � ���������� ���-�� �����
		OutPoints(POINTS, n, fprotok); // ������� ��� ��������� ����� � ���� ���������
		TaskSolving(POINTS, n, fprotok, frez); // ������� ������������ ������
	}
	fin.close(); frez.close(); fprotok.close();
}