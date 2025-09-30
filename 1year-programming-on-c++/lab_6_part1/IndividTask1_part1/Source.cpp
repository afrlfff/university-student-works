#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;

struct StrD
{
	char* pA;
	char Mark;
};

bool GetDataFromFile1(fstream* fin, fstream* fout, StrD* a, unsigned* L1, unsigned* L2) {
	char s; // ���������� ��� ��������� ��������
	char stopSimb; // ������-������������ �� ������ ������ ������� �����
	int k1; // k1 - ���-�� ���� ��������� �������� � ������ (�� ����� ����� ��� ����-�������);
	int k2; // k2 - ���-�� �������� � ����� ������
	bool isEnd = false; // �� ���� ����� ����� �����, �� seekg() �� ����� ��������

	if (!(*fin).is_open()) {
		(*fout) << "������: �������� � ���������  ����� in1.txt";
		return true;
	}

	(*fin) << resetiosflags(ios::skipws);
	(*fin) >> (*a).Mark; cout << "��������� ������: " << (*a).Mark << endl;

	do {
		if ((*fin).eof()) {
			(*fout) << "������: � ����� in1.txt ������ ���� ���� �� 3 �������� ������";
			return true;
		}
		(*fin) >> s;
	} while (s != '\n');

	(*fin) >> stopSimb;
	cout << "��������� ������-������������: " << stopSimb << endl;

	do {
		if ((*fin).eof()) {
			(*fout) << "������: � ����� in1.txt ������ ���� ���� �� 3 �������� ������";
			return true;
		}
		(*fin) >> s;
	} while (s != '\n');

	// ������� �������� �� ������, ����� ��������� ���������� ��������
	// (� ������ ����, ��� ������ ����� ������ �����������) � ������ ������ ������� pA
	k1 = 0; k2 = 0;
	do {
		(*fin) >> s;
		if ((*fin).eof()) {
			isEnd = true;
			break;
		}
		k1++;
		if (s == '.') k2 += 3;
		else k2++;
	} while (!(s == stopSimb || s == '\n'));

	(*a).pA = new char[k2 + 1]; // "+1" - ����� ��� �������� � ����� ������

	if (isEnd) {
		(*fin).close(); (*fin).open("in1.txt", ios::in);
		(*fin).seekg(-k1, ios::end);
	}
	else (*fin).seekg(-k1, ios::cur);

	// ���������� ������� �������� �������
	for (int i = 0; i < k1; i++) {
		(*fin) >> s; (*a).pA[i] = s;
	}

	// ������� � ������ ����� ���� �������� ������ ������
	(*a).pA[k1] = (*a).Mark;

	*L1 = k1; cout << "������ ������ ������: " << k1 << endl;
	*L2 = k2; cout << "������ ����� ������: " << k2 << endl;

	return false;
}

bool GetDataFromFile2(fstream* fin, fstream* fout, StrD* a, unsigned* L1, unsigned* L2) {
	char s; // ���������� ��� ��������� ��������
	int stopNumber = -1; // �����-������������ �� ������ ������ ������� �����
	int k1; // k1 - ���-�� ���� ��������� �������� � ������ (�� ����� ����� ��� ����-�������);
	int k2; // k2 - ���-�� �������� � ����� ������
	bool isEnd = false; // �� ���� ����� ����� �����, �� seekg() �� ����� ��������

	if (!(*fin).is_open()) {
		(*fout) << "������: �������� � ��������� ����� in2.txt";
		return true;
	}

	(*fin) << resetiosflags(ios::skipws);
	(*fin) >> (*a).Mark; cout << "��������� ������: " << (*a).Mark << endl;

	do {
		if ((*fin).eof()) {
			(*fout) << "������: � ����� in2.txt ������ ���� ���� �� 3 �������� ������";
			return true;
		}
		(*fin) >> s;
	} while (s != '\n');

	
	while (1) { // ��������� �����-������������
		(*fin) >> s;
		if ((*fin).eof()) {
			(*fout) << "������: � ����� in2.txt ������ ���� ���� �� 3 �������� ������\n";
			return true;
		}
		else if (s == '\n') {
			(*fout) << "������: �� ������� ������� �����-������������.\n";
			return true;
		}
		else if (s == '0' || s == '1' || s == '2' || s == '3' || s == '4' || s == '5'
			|| s == '6' || s == '7' || s == '8' || s == '9')
		{
			(*fin).unget(); (*fin) >> stopNumber;
			break;
		}
	}

	do {
		if ((*fin).eof()) {
			(*fout) << "������: � ����� in2.txt ������ ���� ���� �� 3 �������� ������";
			return true;
		}
		(*fin) >> s;
	} while (s != '\n');

	// ������� �������� �� ������, ����� ��������� ���������� ��������
	// (� ������ ����, ��� ������ ����� ������ �����������) � ������ ������ ������� pA
	k1 = 0; k2 = 0;
	do {
		(*fin) >> s;
		if ((*fin).eof()) {
			isEnd = true;
			break;
		}
		k1++;
		if (s == '.') k2 += 3;
		else k2++;
	} while (!(s == '\n' || k1 >= stopNumber));

	(*a).pA = new char[k2 + 1]; // "+1" - ����� ��� �������� � ����� ������

	if (isEnd) {
		(*fin).close(); (*fin).open("in2.txt", ios::in);
		(*fin).seekg(-k1, ios::end);
	}
	else (*fin).seekg(-k1, ios::cur);

	// ������ �������� ������ ��������� �������� ������
	for (int i = 0; i < k1; i++) {
		(*fin) >> s;
		(*a).pA[i] = s;
	}

	// ������� � ������ ����� ���� �������� ������ ������
	(*a).pA[k1] = (*a).Mark;

	*L1 = k1; cout << "������ ������ ������: " << k1 << endl;
	*L2 = k2; cout << "������ ����� ������: " << k2 << endl;

	return false;
}

void Solving(StrD* a) {
	unsigned i = 0, count = 0;

	while ((*a).pA[i] != (*a).Mark) {
		if ((*a).pA[i] == '.') count++;
		i++;
	}
	i -= 1; // �.�. �� ����� ����������� ����� �� �� �������, � �� ���������� ������� ������

	while ((i >= 0) && (count > 0 || i >= 2)) {
		if ((*a).pA[i] == '.') {
			(*a).pA[i + count * 2] = (*a).pA[i];
			(*a).pA[i + count * 2 - 1] = (*a).pA[i];
			(*a).pA[i + count * 2 - 2] = (*a).pA[i];
			count--;
		}
		else {
			(*a).pA[i + count * 2] = (*a).pA[i];
		}
		i--;
	}
}

void OutString(fstream* fout, StrD a, unsigned L) {
	for (unsigned i = 0; i < L; i++) {
		(*fout) << a.pA[i]; cout << a.pA[i];
	}
	(*fout) << endl; cout << endl;
}

int main() {
	fstream fin1, fin2, fout;
	StrD a;
	unsigned L1, L2; // ����� ������ � ����� ������
	setlocale(LC_ALL, "rus");

	fout.open("out.txt", ios::out);
	fin1.open("in1.txt", ios::in);
	fout << "������ ��������� 2302\n\n";

	if (!(GetDataFromFile1(&fin1, &fout, &a, &L1, &L2))) {
		fout << "������� ��� ����� in1.txt:\n\n";
		fout << "��������� ������: \t"; cout << "��������� ������: \t";
		OutString(&fout, a, L1);
		Solving(&a);
		fout << "����� ������: \t\t"; cout << "����� ������: \t\t";
		OutString(&fout, a, L2);
		if (a.pA != NULL) delete[] a.pA;
	}

	fout << "\n\n"; cout << "\n\n";
	fin2.open("in2.txt", ios::in);

	if (!(GetDataFromFile2(&fin2, &fout, &a, &L1, &L2))) {
		fout << "������� ��� ����� in2.txt:\n\n";
		fout << "��������� ������: \t"; cout << "��������� ������: \t";
		OutString(&fout, a, L1);
		Solving(&a);
		fout << "����� ������: \t\t"; cout << "����� ������: \t\t";
		OutString(&fout, a, L2);
		if (a.pA != NULL) delete[] a.pA;
	}
	fin1.close();
	fin2.close();
	fout.close();
	return 0;
}
// 123123.qwerty...afweg..12