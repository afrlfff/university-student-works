#pragma once

#include "Money.h"
#include "Stroka.h"

struct Query
{
	Money money;

	Query* next = nullptr;
	Query* prev = nullptr;
};