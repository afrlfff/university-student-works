#ifndef LINE
#define LINE
#include "StrL.h"

struct Line
{
	// next element
	Line* pNext = nullptr;
	// data
	StrL strl;
};


#endif 