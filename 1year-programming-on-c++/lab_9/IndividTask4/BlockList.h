#ifndef BLOCKLIST
#define BLOCKLIST
#include "Block.h"

// ���� � ������ (������ ���� ������ ������ + ������)
class BlockList
{
	// *h = head
	Block* head;
public:
	BlockList();
	Block* get_head();
	void push(char* stroka, unsigned size);
	void out_list(fstream* f);
	void delete_list();
};

#endif

