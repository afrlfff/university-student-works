#pragma once
#include <iostream>

inline bool check_string_for_long(std::string str) {
	for (int i = 0; i < str.size(); i++) {
		if (
			(str[i] >= 48 && str[i] <= 57) ||
			(str[i] == 45 && i == 0)
			) continue;
		return 0;
	}
	return 1;
}
