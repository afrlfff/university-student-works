#pragma once

#include "Query.h"

class QueriesList
{
	Query* head;
	Query* tail;
public:
	unsigned N; // кол-во элементов списка
	unsigned queriesCount; // кол-во запросов

	QueriesList();
	Query* get_head();
	Query* get_tail();
	QueriesList copy();
	void push_back(unsigned nominal, Stroka currecny, unsigned count);
	void change_count(Query* elem, int k);
	void delete_element(Query* elem);
	void out_list(fstream* f);
	void delete_list();
};
