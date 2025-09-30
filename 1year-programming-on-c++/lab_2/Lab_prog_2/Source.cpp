/* Задание: рис. 5.4 (з). Задание 2
*  Автор: Фролов Александр Эдуардович
*  Группа: 2302
*  Версия: 1.1
*/

#include <iostream>
#include <iomanip>
#include <math.h>
using namespace std;

void main(void)
{
	setlocale(LC_CTYPE, "rus"); // русский язык в консоли
	float x, a, n, y;
	cout << "Автор: Фролов Александр Эдуардович \n\n";

	cout << "Введите значение а: ";
	cin >> a;
	cout << "Введите значение х: ";
	cin >> x;

	n = abs(a) * 4;
	if (remainder(x, n) < 0) {
		x = remainder(x, n) + n;
	}
	else {
		x = remainder(x, n);
	}

	if (a > 0) {
		if ((0 <= x) && (x < (2 * a))) {
			y = sqrt((a * a) - (x - a) * (x - a));
			cout << "y = " << fixed << setprecision(3) << y << "\n";
		}
		else if (x == (2 * a)) {
			cout << "y принадлежит отрезку ["<< fixed <<
				setprecision(3) << -a << ";0]\n";
		}
		else if (((2 * a) < x) && (x <= (3 * a))) {
			y = -(x - 2*a) - a;
			cout << "y = " << fixed << setprecision(3) << y << "\n";
		}
		else{
			y = 2*(x-4*a);
			cout << "y = " << fixed << setprecision(3) << y << "\n";
		}
	}
	else if (a < 0) {
		a *= -1;
		if ((0 <= x) && (x < a)) {
			y = 2 * x;
			cout << "y = " << fixed << setprecision(3) << y << "\n";
		}
		else if ((a <= x) && (x < 2 * a)) {
			y = -1*(x - a) + 2*a;
			cout << "y = " << fixed << setprecision(3) << y << "\n";
		}
		else if (x == (2 * a)) {
			cout << "y принадлежит отрезку [0;" << a << "]\n";
		}
		else{
			y = -1*(sqrt((a * a) - (x - 3*a) * (x - 3*a)));
			cout << "y = " << fixed << setprecision(3) << y << "\n";
		}
	}
	else { // a == 0
		if (x == 0) {
			cout << "y = 0";
		}
		else {
			cout << "Значение функции определить невозможно";
		}
	}	
}