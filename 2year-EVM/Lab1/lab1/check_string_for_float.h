#pragma once
#include <iostream>

inline bool check_string_for_float(std::string str) {
	unsigned short dotCount = 0;
	for (int i = 0; i < str.size(); i++) {
		if (str[i] == 44) {
			if (i == 0 || i == (str.size() - 1) || dotCount > 1)
				return 0;
			else
				dotCount++;
		}
		else if (
			(str[i] >= 48 && str[i] <= 57) ||
			(str[i] == 45 && i == 0)
			)
			continue;
		else
			return 0;
	}
	return 1;
}
