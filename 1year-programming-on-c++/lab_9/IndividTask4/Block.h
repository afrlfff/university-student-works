#ifndef BLOCK
#define BLOCK
#include "StrM.h"

const unsigned N = 5; // ���-�� �������� � �����

struct Block
{
	StrM str; // data
	Block* next = nullptr;
};

#endif