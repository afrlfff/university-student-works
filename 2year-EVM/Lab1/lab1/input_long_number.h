#pragma once
#include <iostream>
#include <string>

#include "check_string_for_long.h"

inline long input_long_number()
{
	std::string str;
	long number;

	while (1)
	{
		std::cin >> str;
		if (check_string_for_long(str))
		{
			try
			{
				number = stol(str);
				break;
			}
			catch (std::exception)
			{
				std::cout << "������� ������������ �����!\n"
					<< "���������� ��� ���: ";
			}
		}
		else
		{
			std::cout << "������� ������������ �����!\n"
				<< "���������� ��� ���: ";
		}
	}
	return number;
}