#pragma once
#include <iostream>
#include "constants.h"

void out_machine_code(std::string strCode, const std::string& key) {
	if (key == "long")
	{
		for (int i = 0; i < strCode.size(); i++)
		{
			if (i == 1)
				std::cout << " | ";
			std::cout << strCode[i];
		}
	}
	else if (key == "float")
	{
		for (int i = 0; i < strCode.size(); i++)
		{
			if (i == 1 || i == (FLOAT_BITS_P + 1))
				std::cout << " | ";
			std::cout << strCode[i];
		}
	}
}