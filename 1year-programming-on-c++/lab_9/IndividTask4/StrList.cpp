#include "lib.h"
#include "StrList.h"

StrList::StrList() { head = nullptr; }

Stroka* StrList::get_head() { return head; }
void StrList::push(BlockList data)
{
	if (head == nullptr)
	{
		head = new Stroka;
		head->data = data;
	}
	else
	{
		Stroka* tmp = head;
		while (tmp->next != nullptr) {
			tmp = tmp->next;
		}
		tmp->next = new Stroka;
		tmp->next->data = data;
	}
}
void StrList::out_list(fstream* f)
{
	Stroka* tmp = head;
	while (tmp != nullptr)
	{
		tmp->data.out_list(f);
		cout << "\n\t|\n\tV\n"; *f << "\n\t|\n\tV\n";
		tmp = tmp->next;
	}
	cout << "\tNULL\n\n"; *f << "\tNULL\n\n";
}
void StrList::delete_list()
{
	Stroka* tmp;
	while (head != nullptr)
	{
		tmp = head;
		head = head->next;
		tmp->data.delete_list(); // delete data
		delete tmp; // delete element
	}
}