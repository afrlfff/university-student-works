#ifndef STROKA
#define STROKA
#include "BlockList.h"

// ������� ������ �����
struct Stroka
{
	BlockList data;
	Stroka* next = nullptr;
};

#endif
