#pragma once

#include "QueriesList.h"
#include "Stroka.h"

struct Client
{
	Stroka Name;
	Stroka Adress;
	QueriesList Queries;
	Client* next = nullptr;
	Client* prev = nullptr;
};