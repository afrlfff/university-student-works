/* ������� #17. ������������ ������ #4.
*  �����: ������ ��������� ����������
*  ������: 2302
*  ������: 1.1
*/

#include <iostream>
#include <fstream>
using namespace std;

void main(void)
{
	setlocale(LC_CTYPE, "rus"); // ������� ���� � �������
	const unsigned N = 15;
	float A[N], B[N], C[N];
	int L, i, ind_B, ind_C;
	fstream f;
	cout << "�����: ������ ��������� ���������� \n\n";
	f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_1/in.txt", ios::in);

	if (!f.is_open()) cout << "�������� � ��������� ����� :(\n";
	else {
		f >> L;
		if (f.eof()) {
			cout << "� �������� ����� ������������ ������\n"; // ���� <2 ��������
			f << "� �������� ����� ������������ ������\n"; // ���� <2 ��������
		} else {
			if (L < 0) L = 0;
			i = 0;
			while (i < L) {
				f >> A[i];
				i++;
				if ((f.eof()) || (i >= N)) { L = i; break; }
			}
			f.close(); f.open("C:/Users/DNS/Desktop/c++/lab_4/Lab4_prog_1/out.txt", ios::out);
			f << "�����: ������ ��������� ���������� \n\n";

			cout << "����� ��������� � �������� ������� = " << L << endl;
			f << "����� ��������� � �������� ������� = " << L << endl;

			cout << "�������� ������ �: [";
			f << "�������� ������ �: [";
			for (i = 0; i < L; i++) {
				cout << A[i]; f << A[i];
				if (i != (L - 1)) {
					cout << ", "; f << ", ";
				}
			}
			cout << "]" << endl; f << "]" << endl;
			
			ind_B = 0;
			for (i = 0; i < L; i++) {
				// �������� ������ B ����� �������������� ������� ������� �
				if (A[i] > 0) {
					B[ind_B] = A[i];
					ind_B++;
				}
			} for (i = ind_B; i < L; i++) {
				// �������� ������ �������� ������� B �������������� �������
				B[i] = -1;
			}
			ind_C = 0;
			for (i = (L-1); i >= 0; i--) {
				// �������� ������ � ����� �������������� ������� ������� �
				if (A[i] < 0) {
					C[ind_C] = A[i];
					ind_C++;
				}
			} for (i = ind_C; i < L; i++) {
				// �������� ������ �������� ������� � �������������� �������
				C[i] = 1;
			}
			
			cout << "������ �: [";
			f << "������ �: [";
			for (i = 0; i < L; i++) {
				// ������ ��� ������������� ����� ������� �
				if (B[i] < 0) break;
				else {
					cout << B[i]; f << B[i];
					if (i != (ind_B - 1)) {
						cout << ", "; f << ", ";
					}
				}
			}
			cout << "]" << endl << "������ C: [";
			f << "]" << endl << "������ C: [";
			for (i = 0; i < L; i++) {
				// ������ ��� ������������� ����� ������� �
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