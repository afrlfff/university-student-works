#pragma once

#include "lib.h"
#include "Stroka.h"
#include "Money.h"

class FundList
{
	Money* head, * tail;
public:
	unsigned R; // сумма фонда
	unsigned N; // кол-во номиналов в Фонде

	FundList();
	Money* get_head();
	Money* get_tail();
	Money* get_element_by_nominal(unsigned nominal);
	FundList copy();
	void push_back(unsigned nominal, Stroka currecny, unsigned count);
	void delete_element(Money* elem);
	void change_count(Money* elem, int k);
	void out_list(fstream* f);
	void delete_list();
};
