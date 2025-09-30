#pragma once
#include <iostream>
#include <math.h>

#include "constants.h"
#include "to_binary.h"

// convert float to machine code string
std::string float_to_machine_code(float f)
{
	// 127 for float / 1023 for double, etc.
	uint16_t HALF_OF_P = (pow(2, FLOAT_BITS_P) / 2) - 1;
	std::string result;

	if (f == 0)
	{
		for (uint8_t i = 0; i < FLOAT_SIZE; i++)
			result = result + '0';
	}
	else
	{
		int int_part = int(abs(f)); // целая часть
		float frac_part = abs(f) - int_part; // дробная часть

		std::string bin_int_part = to_binary(int_part);
		std::string bin_frac_part;
		std::string M, P;
		float b = frac_part; // для посчета bin_frac_part

		if (int_part == 0) // порядок будет отрицательным
		{
			uint8_t tmp = 0;

			// записываем в bin_frac_part двоичное представление дробной части
			for (uint8_t k = 0; k < (FLOAT_BITS_M + 1); k++)
			{
				b *= 2;
				if (b >= 1) {
					tmp = k + 1;
					k = 0;
					bin_frac_part.clear();
					bin_frac_part = '1';
					b -= 1;
				}
				else bin_frac_part += '0';
			}

			P = to_binary(HALF_OF_P - tmp);
			while (P.size() != FLOAT_BITS_P)
				P = '0' + P;

			M = bin_frac_part;
			M.erase(0, 1); // удаляем 1 символ с 0 индекса
		}
		else { // порядок будет положительным

			// записываем в bin_frac_part двоичное представление дробной части
			for (uint16_t k = 0; k < (FLOAT_BITS_M - bin_int_part.size() + 1); k++) {
				b *= 2;
				if (b >= 1) {
					bin_frac_part += '1';
					b -= 1;
				}
				else bin_frac_part += '0';
			}
			M = bin_int_part + bin_frac_part;
			M.erase(0, 1); // // удаляем 1 символ с 0 индекса
			P = to_binary(HALF_OF_P + bin_int_part.size() - 1);
			while (P.size() != FLOAT_BITS_P)
				P = '0' + P;
		}

		if (f >= 0) result = '0';
		else result = '1';

		result += P + M;
	}

	return result;
}
