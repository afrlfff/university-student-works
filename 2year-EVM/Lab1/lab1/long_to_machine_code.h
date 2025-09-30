#pragma once
#include <iostream>

#include "constants.h"
#include "to_binary.h"

// convert long to machine code string
std::string long_to_machine_code(long a)
{
	std::string result;
	if (a == 0) {
		for (int i = 0; i < LONG_SIZE; i++)
		{
			result += '0';
		}
	}
	else {
		result = to_binary(abs(a));

		for (int i = result.size(); i < (LONG_SIZE - 1); i++) {
			result = '0' + result;
		}	

		if (a >= 0)
			result = '0' + result;
		else
			result = '1' + result;
	}

	return result;
}