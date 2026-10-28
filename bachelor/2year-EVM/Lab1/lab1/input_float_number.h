#pragma once
#include <iostream>
#include <string>

#include "check_string_for_float.h"

inline double input_float_number()
{
	std::string str;
	double number;

	while (1)
	{
		std::cin >> str;
		if (check_string_for_float(str)) {
			try
			{
				number = stof(str);
				break;
			}
			catch (std::exception)
			{
				std::cout
					<< "Введено некорректное число!\n"
					<< "Попробуйте еще раз: ";
			}

		}
		else
		{
			std::cout
				<< "Введено некорректное число!\n"
				<< "Попробуйте еще раз: ";
		}
	}
	return number;
}