/* ������� #1: P(x) = 9.09x^8 + 9.09x^4 + 9.09x^2
*  ������� #2: P(x) = 8.243x^24 + 725.6x^20 + 186.41x^16
*  ������� #3: ����������� ���������� �1 � �2.
*  �����: ������ ��������� ����������
*  ������: 2302
*  ������: 1.1
*  ����: ������: 11.09.2022 ���������: 14.09.2022
*/

#include <iostream>
#include <iomanip>
using namespace std;

void main(void)
{
	setlocale(LC_CTYPE, "rus"); // ������� ���� � �������
	float x, P1, P2, P, y, n;
	cout << "�����: ������ ��������� ���������� \n\n";

	cout << "������� �: ";
	cin >> x;

	// ������� #1.
	cout << "������� #1. \n"
		<< "P(x) = 9.09x^8 + 9.09x^4 + 9.09x^2 \n";
	n = 9.09;
	y = x * x;
	P1 = n * y;
	cout << "1� ���: � = " << fixed << setprecision(15) << P1 << "\n";
	P1 = (P1 * y) + n;
	cout << "2� ���: � = " << fixed << setprecision(15) << P1 << "\n";
	P1 = (P1 * y) + n;
	cout << "3� ���: � = " << fixed << setprecision(15) << P1 << "\n";
	P1 = P1 * y;
	cout << "4� ���: � = " << fixed << setprecision(15) << P1 << "\n";
	cout << "��������� ��� x = " << fixed << setprecision(3) << x << ": \n"
		<< fixed << setprecision(15) << P1 << "\n\n";

	// ������� #2.
	cout << "������� #2. \n"
		<< "P(x) = 8.243x^24 + 725.6x^20 - 186.41x^16 \n"
		<< "������� �: ";
	y = x * x * x * x;
	P2 = (8.243 * y) + 725.6;
	cout << "1� ���: � = " << fixed << setprecision(15) << P2 << "\n";
	P2 = (P2 * y) - 186.41;
	cout << "2� ���: � = " << fixed << setprecision(15) << P2 << "\n";
	P2 = P2 * y * y * y * y;
	cout << "3� ���: � = " << fixed << setprecision(15) << P2 << "\n";
	cout << "��������� ��� x = " << fixed << setprecision(3) << x << ": \n"
		<< fixed << setprecision(15) << P2 << "\n\n";

	// ������� #3.
	cout << "������� #3. \n"
		<< "����������� ���������� �1 � �2. \n";
	P = P1 * P2;
	cout << "���������: \n" << fixed << setprecision(15) << P << "\n";
}