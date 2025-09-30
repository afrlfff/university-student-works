#pragma once

#include <iostream>
#include "constants.h"

void replace_two_group_of_bytes(std::string& str, int8_t digit1, int8_t digit2, int8_t count)
{
	uint8_t SIZE = str.size();
	int8_t i = (SIZE - 1) - digit1 + 1;
	int8_t j = (SIZE - 1) - digit2 + 1;

	for (int8_t k = 0; k < count; k++, i--, j--)
	{
		std::swap(str[i], str[j]);
	}
}