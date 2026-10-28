#pragma once

#include "StrL.h"

const unsigned BLOCK_SIZE = 5;

struct StrBlock
{
	StrL str;
	StrBlock* next = nullptr;
};
