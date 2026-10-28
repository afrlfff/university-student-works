#ifndef BLOCK
#define BLOCK
#include "StrM.h"

const unsigned N = 5; // кол-во символов в блоке

struct Block
{
	StrM str; // data
	Block* next = nullptr;
};

#endif