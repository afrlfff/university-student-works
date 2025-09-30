#pragma once

#include "Stroka.h"

struct Money
{
	unsigned nominal = 0;
	Stroka currency; // валюта
	unsigned count = 0; // кол-во купюр данного номинала

	Money* next = nullptr;
	Money* prev = nullptr;
};
