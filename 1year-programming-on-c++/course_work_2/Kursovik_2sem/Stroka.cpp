#include "Stroka.h"

Stroka::Stroka()
{
	head = nullptr;
}
StrBlock* Stroka::get_head()
{
	return head;
}
void Stroka::push_back(char* stroka, unsigned L)
{
	if (head == nullptr)
	{
		head = new StrBlock;

		head->str.L = L;
		head->str.pA = new char[L];
		for (unsigned i = 0; i < L; i++)
		{
			head->str.pA[i] = stroka[i];
		}
	}
	else
	{
		StrBlock* tmp = head;
		while (tmp->next != nullptr)
		{
			tmp = tmp->next;
		}
		tmp->next = new StrBlock;

		tmp->next->str.L = L;
		tmp->next->str.pA = new char[L];
		for (unsigned i = 0; i < L; i++)
		{
			tmp->next->str.pA[i] = stroka[i];
		}
	}
}
Stroka Stroka::copy()
{
	Stroka B;
	StrBlock* tmp = head;
	while (tmp != nullptr) {
		B.push_back(tmp->str.pA, tmp->str.L);
		tmp = tmp->next;
	}
	return B;
}
void Stroka::out_list(fstream* f)
{
	StrBlock* tmp = head;
	while (tmp != nullptr)
	{
		for (unsigned i = 0; i < tmp->str.L; i++)
		{
			*f << tmp->str.pA[i];
		}
		*f << " -> ";
		tmp = tmp->next;
	}
	*f << "NULL";
}

void Stroka::delete_list()
{
	StrBlock* tmp;
	while (head != nullptr)
	{
		tmp = head;
		head = head->next;
		delete[] tmp->str.pA;
		delete tmp;
	}
}