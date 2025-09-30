#include <iostream>
#include <vector>
#include <math.h>
#include <string>
#include <iomanip>

#include "input_long_number.h"
#include "input_float_number.h"
#include "long_to_machine_code.h"
#include "float_to_machine_code.h"
#include "out_machine_code.h"
#include "constants.h"
#include "input_two_group_of_bytes.h"
#include "replace_two_group_of_bytes.h"

int main()
{
	setlocale(LC_ALL, "ru");

	long l_number;
	float f_number;

	// ==========
	// ========== Entering long ========== //
	// ==========

	std::cout
		<< "Введите число типа long int"
		<< "(целое число от -2^" << (LONG_SIZE - 1)
		<< " до 2^" << (LONG_SIZE - 1) << ") : ";

	l_number = input_long_number();
	std::cout << "Введенное вами число: " << l_number << "\n\n";

	// ==========
	// ========== Entering float ========== //
	// ==========

	std::cout
		<< "Введите число типа float"
		<< "(целое число от -2^" << (FLOAT_SIZE - 1)
		<< " до 2^" << (FLOAT_SIZE - 1) << ")\n"
		<< "(целую и дробную часть отделять запятой) : ";

	f_number = input_float_number();
	std::cout
		<< "Введенное вами число: " << std::fixed
		<< std::setprecision(8) << f_number << "\n\n";

	// ==========
	// ========== Conversion to machine code ========== //
	// ==========

	std::string l_machine_code = long_to_machine_code(l_number);
	std::string f_machine_code = float_to_machine_code(f_number);

	std::cout << "Результат для переменной long int: ";
	out_machine_code(l_machine_code, "long");
	std::cout << "\n\nРезультат для переменной float: ";
	out_machine_code(f_machine_code, "float");
	std::cout << "\n\n";

	// ==========
	// ========== Individual task ========== //
	// ==========
	
	int8_t digit1, digit2, count;
	int8_t* arrTmp = new int8_t[3];

	std::cout << "Индивидуальное задание.\n" <<
		"Требуется поменять местами две группы рядом стоящих бит.\n";
	
	std::cout << "Преобразуем long-число.\n";
	
	arrTmp = input_two_group_of_bytes("long");
	digit1 = arrTmp[0];
	digit2 = arrTmp[1];
	count = arrTmp[2];
	replace_two_group_of_bytes(l_machine_code, digit1, digit2, count);
	std::cout << "Результат: ";
	out_machine_code(l_machine_code, "long");
	std::cout << "\n\n";

	std::cout << "Преобразуем float-число.\n";

	arrTmp = input_two_group_of_bytes("float");
	digit1 = arrTmp[0];
	digit2 = arrTmp[1];
	count = arrTmp[2];
	replace_two_group_of_bytes(f_machine_code, digit1, digit2, count);
	std::cout << "Результат: ";
	out_machine_code(f_machine_code, "float");
	std::cout << "\n\n";
	
	delete[] arrTmp;
	return 1;
}