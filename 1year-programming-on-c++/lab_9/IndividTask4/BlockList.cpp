#include "lib.h"
#include "BlockList.h"

BlockList::BlockList() { head = nullptr; }
Block* BlockList::get_head() { return head; }
void BlockList::push(char* stroka, unsigned size)
{
	if (head == nullptr)
	{
		head = new Block;
		head->str.pA = new char[N + 1]; // size <= N
		for (unsigned i = 0; i < size; i++)
		{
			head->str.pA[i] = stroka[i];
		}
		head->str.pA[size] = head->str.Mark;
	}
	else
	{
		Block* tmp = head;
		while (tmp->next != nullptr) {
			tmp = tmp->next;
		}
		tmp->next = new Block;
		tmp->next->str.pA = new char[N + 1]; // size <= N
		for (unsigned i = 0; i < size; i++)
		{
			tmp->next->str.pA[i] = stroka[i];
		}
		tmp->next->str.pA[size] = tmp->str.Mark;
	}
}
void BlockList::out_list(fstream* f)
{
	Block* tmp = head;
	cout << '\t'; *f << '\t';
	while (tmp != nullptr)
	{
		for (unsigned i = 0; i < N; i++)
		{
			if (tmp->str.pA[i] == tmp->str.Mark) break;
			cout << tmp->str.pA[i];
			*f << tmp->str.pA[i];
		}
		cout << " --> "; *f << " --> ";
		tmp = tmp->next;
	}
	cout << "NULL"; *f << "NULL";
}
void BlockList::delete_list()
{
	Block* tmp;
	while (head != nullptr)
	{
		tmp = head;
		head = head->next;
		delete[] tmp->str.pA; // delete data
		delete tmp; // delete element
	}
}