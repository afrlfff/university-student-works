#pragma once
#include <iostream>

template<typename T>
std::string to_binary(T a) {
	if (a == 0)
		return "0";
	T b = a;
	std::string result;
	while (b > 0) {
		if (b % 2 == 0)
			result = '0' + result;
		else
			result = '1' + result;
		b /= 2;
	}

	return result;
}