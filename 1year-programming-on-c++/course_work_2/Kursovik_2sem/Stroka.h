#pragma once

#include "lib.h"
#include "StrBlock.h"

class Stroka
{
	StrBlock* head;
public:
	Stroka();
	StrBlock* get_head();
	Stroka copy();
	void push_back(char* stroka, unsigned L);
	void out_list(fstream* f);
	void delete_list();
};
