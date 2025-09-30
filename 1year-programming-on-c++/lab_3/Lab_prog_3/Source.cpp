/* ������� #5. ������������ ������ #3.
*  �����: ������ ��������� ����������
*  ������: 2302
*  ������: 1.2
*/

#include <iostream>
#include <iomanip>
#include <fstream>
using namespace std;

void main(void)
{
	setlocale(LC_CTYPE, "rus"); // ������� ���� � �������
	unsigned i;
	double x, a, eps, S;
	fstream f;
	cout << "�����: ������ ��������� ���������� \n\n";

	cout << "������� �������� ���������� �: ";
	cin >> x;

	cout << "������� �������� ���������� eps: ";
	cin >> eps;
	i = 1;
	while (((eps > (1e-10)) || (eps <= 0)) && (i < 3))
	{
		cout << "������������ �������� eps. ������� eps ��� ���: ";
		cin >> eps;
		i++;
	}
	if (((eps > (1e-10)) || (eps <= 0))){
		cout << "�� �� ������ ������ ���������� eps � 3� �������!!! ����!!!\n";
	}
	else { // ������� ������
		f.open("solve.txt", ios::out);
		i = 0; a = 1; S = a;
		cout << "\n ��� x = " << x << " � eps = " << eps << " ������� �������� ��������� �������: " << endl;
		cout << "|" << "________" << "i" << "_______" << "|" << "________" << "a"
			<< "_______" << "|" << "________" << "S" << "_______" << "|" << endl;
		f << "\n ��� x = " << x << " � eps = " << eps << " ������� �������� ��������� �������: " << endl;
		f << "|" << "________" << "i" << "_______" << "|" << "________" << "a"
			<< "_______" << "|" << "________" << "S" << "_______" << "|" << endl;

		cout << "|" << setw(9) << i << setw(8) << "|" << setw(13) << setprecision(5) << a
			<< setw(4) << "|" << setw(13) << setprecision(5) << S << setw(4) << "|" << endl;
		f << "|" << setw(9) << i << setw(8) << "|" << setw(13) << setprecision(5) << a
			<< setw(4) << "|" << setw(13) << setprecision(5) << S << setw(4) << "|" << endl;

		while (((abs(a)) >= eps) && (i < 1000)) // while a �� ����������� [-eps; eps] AND i < 1000
		{
			a *= (x * (i + 2.0)) / (i + 1.0) / (i + 1.0); // a *= x(i+2) / (i+1)^2
			S += a;
			cout << "|" << setw(9) << (i+1) << setw(8) << "|" << setw(13) << setprecision(5) << a
				<< setw(4) << "|" << setw(13) << setprecision(5) << S << setw(4) << "|" << endl;
			f << "|" << setw(9) << (i+1) << setw(8) << "|" << setw(13) << setprecision(5) << a
				<< setw(4) << "|" << setw(13) << setprecision(5) << S << setw(4) << "|" << endl;
			i++;
		}
		cout << "\n ������ ���������� ����� = " << i << '\n';
		f << "\n ������ ���������� ����� = " << i << '\n';
		f.close();
	}
}