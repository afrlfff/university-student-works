#pragma once

#include <iostream>
#include <string>
#include "check_string_for_long.h"
#include "constants.h"

int8_t* input_two_group_of_bytes(std::string key)
{
	uint8_t SIZE = LONG_SIZE;
	if (key == "long")
		SIZE = LONG_SIZE;
	if (key == "float")
		SIZE = FLOAT_SIZE;


	std::string stmp1, stmp2;
	int8_t* result = new int8_t[3]; // digit1, digit2, count
	while (true)
	{
		try
		{
			std::cout << "Введите через пробел номера разрядов первой и второй группы " <<
				"(от 1 до " << int(SIZE) << "): ";
			std::cin >> stmp1 >> stmp2;

			// function "check_string_for_long" will also check for int number
			if (check_string_for_long(stmp1) && check_string_for_long(stmp2))
			{
				result[0] = stoi(stmp1);
				result[1] = stoi(stmp2);
			}
			else throw std::exception();


			std::cout << "Введите количество символов в группе (не меньше 1): ";
			std::cin >> stmp1;

			// function "check_string_for_long" will also check for int number
			if (check_string_for_long(stmp1))
			{
				result[2] = stoi(stmp1);
			}
			else throw std::exception();

			if (result[0] < 1 || result[0] > SIZE ||
				result[1] < 1 || result[1] > SIZE ||
				result[2] < 1 ||
				result[2] > (SIZE - result[0] + 1) ||
				result[2] > (SIZE - result[1] + 1)
				)
				throw std::exception();

			break;
		}
		catch (std::exception)
		{
			std::cout << "Введены некорректные данные. Попробуйте еще раз.\n";
		}
	}
	return result;
}