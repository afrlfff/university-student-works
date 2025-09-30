#ifndef STRLIST
#define STRLIST
#include "Stroka.h"

// список строк
class StrList
{
	Stroka* head;
public:
	StrList();
	Stroka* get_head();
	void push(BlockList data);
	void out_list(fstream* f);
	void delete_list();
};

#endif