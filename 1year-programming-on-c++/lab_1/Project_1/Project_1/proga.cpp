/* Задание #1: P(x) = 9.09x^8 + 9.09x^4 + 9.09x^2
*  Задание #2: P(x) = 8.243x^24 + 725.6x^20 + 186.41x^16
*  Задание #3: Перемножить результаты х1 и х2.
*  Автор: Фролов Александр Эдуардович
*  Группа: 2302
*  Версия: 1.1
*  Дата: начало: 11.09.2022 окончание: 14.09.2022
*/

#include <iostream>
#include <iomanip>
using namespace std;

void main(void)
{
	setlocale(LC_CTYPE, "rus"); // русский язык в консоли
	float x, P1, P2, P, y, n;
	cout << "Автор: Фролов Александр Эдуардович \n\n";

	cout << "Введите х: ";
	cin >> x;

	// Задание #1.
	cout << "Задание #1. \n"
		<< "P(x) = 9.09x^8 + 9.09x^4 + 9.09x^2 \n";
	n = 9.09;
	y = x * x;
	P1 = n * y;
	cout << "1й шаг: Р = " << fixed << setprecision(15) << P1 << "\n";
	P1 = (P1 * y) + n;
	cout << "2й шаг: Р = " << fixed << setprecision(15) << P1 << "\n";
	P1 = (P1 * y) + n;
	cout << "3й шаг: Р = " << fixed << setprecision(15) << P1 << "\n";
	P1 = P1 * y;
	cout << "4й шаг: Р = " << fixed << setprecision(15) << P1 << "\n";
	cout << "Результат для x = " << fixed << setprecision(3) << x << ": \n"
		<< fixed << setprecision(15) << P1 << "\n\n";

	// Задание #2.
	cout << "Задание #2. \n"
		<< "P(x) = 8.243x^24 + 725.6x^20 - 186.41x^16 \n"
		<< "Введите х: ";
	y = x * x * x * x;
	P2 = (8.243 * y) + 725.6;
	cout << "1й шаг: Р = " << fixed << setprecision(15) << P2 << "\n";
	P2 = (P2 * y) - 186.41;
	cout << "2й шаг: Р = " << fixed << setprecision(15) << P2 << "\n";
	P2 = P2 * y * y * y * y;
	cout << "3й шаг: Р = " << fixed << setprecision(15) << P2 << "\n";
	cout << "Результат для x = " << fixed << setprecision(3) << x << ": \n"
		<< fixed << setprecision(15) << P2 << "\n\n";

	// Задание #3.
	cout << "Задание #3. \n"
		<< "Перемножить результаты х1 и х2. \n";
	P = P1 * P2;
	cout << "Результат: \n" << fixed << setprecision(15) << P << "\n";
}