/* ������� #17. ������������ ������ #4.
*  �����: ������ ��������� ����������
*  ������: 2302
*  ������: 2.1
*/

#include <iostream>
#include <fstream>
using namespace std;

int main()
{
	setlocale(LC_CTYPE, "rus"); // ������� ���� � �������
	float *A, *B, *C, tmp;
	float *p, *q;
	int L, i, kp, ko;
	fstream f;
	cout << "�����: ������ ��������� ���������� \n\n";
	f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_2/in.txt", ios::in);

	if (!f.is_open()) cout << "�������� � ��������� ����� :(\n";
	else {
		if (!f.eof()) {
			L = 0;
			while ((f >> tmp) && (L < 15)) L++;
		}
		A = new float[L+1];
		if (A == NULL) {
			cout << "�������� � ���������� ������ ��� ������� A. \n";
			f << "�������� � ���������� ������ ��� ������� A. \n";
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
		f << "�����: ������ ��������� ���������� \n\n";

		cout << "����� ��������� � �������� ������� = " << L << endl;
		f << "����� ��������� � �������� ������� = " << L << endl;

		cout << "�������� ������ �: [";
		f << "�������� ������ �: [";
		for (p = A; p != A + L; p++) {
			cout << *p; f << *p;
			if ((p-A) != (L - 1)) {
				cout << ", "; f << ", ";
			}
		}
		cout << "]" << endl; f << "]" << endl;

		B = new float[kp];
		if (B == NULL) {
			cout << "�������� � ���������� ������ ��� ������� B. \n";
			f << "�������� � ���������� ������ ��� ������� B. \n";
			return 0;
		}
		for (p = A, q = B; p != A + L; p++) {
			// �������� ������ B ����� �������������� ������� ������� �
			if (*p > 0) {
				*q = *p;
				q++;
			}
		}
		cout << "������ �: ["; f << "������ �: [";
		for (p = B; p != (B + kp); p++) {
			cout << *p; f << *p;
			if (p != (B + kp - 1)) {
				cout << ", "; f << ", ";
			}
		}
		cout << "]" << endl; f << "]" << endl;

		C = new float[ko];
		if (C == NULL) {
			cout << "�������� � ���������� ������ ��� ������� C. \n";
			f << "�������� � ���������� ������ ��� ������� C. \n";
			return 0;
		}
		for (p = A+L-1, q = C; p != A-1; p--) {
			// �������� ������ C ����� �������������� ������� ������� �
			if (*p < 0) {
				*q = *p;
				q++;
			}
		}
		cout << "������ C: ["; f << "������ C: [";
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