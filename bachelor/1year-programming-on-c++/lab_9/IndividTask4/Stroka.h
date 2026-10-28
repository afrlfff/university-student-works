#ifndef STROKA
#define STROKA
#include "BlockList.h"

// элемент списка строк
struct Stroka
{
	BlockList data;
	Stroka* next = nullptr;
};

#endif
