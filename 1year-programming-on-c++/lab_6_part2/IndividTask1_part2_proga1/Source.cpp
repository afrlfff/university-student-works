#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;

class StrL {
	char* pStroka;
	unsigned L;
public:
	void set_pStroka()
	{
		cout << "������ ��������. \n";
		pStroka = new char[L];
	}
	void set_L(unsigned k)
	{
		L = k;
	}

	// ��������������� �������
	void GetBeginOfStr(fstream* f, int k, bool isEnd)
	{
		if (isEnd) {
			f->close(); f->open("in3.txt", ios::in);
			f->seekg(-k, ios::end);
		}
		else f->seekg(-k, ios::cur);
	}

	bool GetStr(fstream* fin, fstream* fout)
	{
		char s; // ���������� ��� ��������� ��������
		char stopSimbol; // ������-������������ �� ������ ������ ������� �����
		int k; // k - ���-�� ���� ��������� �������� � ������ (�� ����� ����� ��� ����-�������);
		bool isEnd = false; // �� ���� ����� ����� �����, �� seekg() �� ����� ��������

		if (!(*fin).is_open()) {
			(*fout) << "������: �������� � ��������� ����� in3.txt.\n";
			return true;
		}

		(*fin) << resetiosflags(ios::skipws);
		(*fin) >> stopSimbol;
		do {
			if ((*fin).eof()) {
				(*fout) << "������: � ����� in3.txt ������ ���� ���� �� 2 �������� ������";
				return true;
			}
			(*fin) >> s;
		} while (s != '\n');

		// �������� �� ������ ������, ����� ��������� ���������� ��������
		k = 0;
		do {
			(*fin) >> s;
			if (fin->eof()) {
				isEnd = true;
				break;
			}
			if (s == stopSimbol) {
				fin->unget();
				break;
			}
			k++;
		} while (!(s == '\n'));

		set_L(k);
		set_pStroka();

		// ������� � ������ ��������� ������ �����
		GetBeginOfStr(fin, k, isEnd);

		// ���������� ������� pStroka �������� �������
		for (int i = 0; i < k; i++) {
			(*fin) >> s; pStroka[i] = s;
		}

		// ������� � ������ ��������� ������ ����� ��� ���������� ������ ����. �������
		GetBeginOfStr(fin, k, isEnd);

		return false;
	}

	void Solving()
	{
		int i;
		unsigned count = 0; // ���������� ����� � ������
		char* pStroka2 = new char[L];

		for (unsigned j = 0; j < L; j++) {
			pStroka2[j] = pStroka[j];
			if (pStroka[j] == '.') count++;
		}
		i = L - 1; // ������ ���������� ������� � �������� ������

		set_L(L + count * 2);
		delete[] pStroka; cout << "������ �����������. \n";
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

	void Out(fstream* fout)
	{
		for (unsigned i = 0; i < L; i++) {
			(*fout) << pStroka[i];
		}
		(*fout) << endl;
	}

	~StrL()
	{
		if (pStroka != NULL) delete[] pStroka;
		cout << "������ �����������. \n";
	}

};

int main() {
	setlocale(LC_ALL, "rus");

	fstream fin, fout;
	StrL stroka;

	fin.open("in3.txt", ios::in);
	fout.open("out3.txt", ios::out);
	fout << "������ ��������� 2302\n\n";

	if (!(stroka.GetStr(&fin, &fout))) {
		fout << "������� ��� ����� in3.txt:\n\n��������� ������: \t";
		stroka.Out(&fout);
		stroka.Solving();
		fout << "����� ������: \t\t";
		stroka.Out(&fout);
	}

	fin.close();
	fout.close();
	return 0;
}