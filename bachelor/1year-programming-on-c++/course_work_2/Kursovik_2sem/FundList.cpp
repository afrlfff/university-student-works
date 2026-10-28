#include "lib.h"
#include "FundList.h"

FundList::FundList()
{
	head = nullptr;
	tail = nullptr;
	R = 0; N = 0;
}
Money* FundList::get_head()
{
	return head;
}
Money* FundList::get_tail()
{
	return tail;
}
Money* FundList::get_element_by_nominal(unsigned nominal)
{
	Money* tmp = head;
	while (tmp != nullptr && tmp->nominal != nominal) {
		tmp = tmp->next;
	}
	return tmp;
}
void FundList::push_back(unsigned nominal, Stroka currecny, unsigned count)
{
	R += (nominal * count);
	N += 1;
	if (head == nullptr)
	{
		head = new Money;
		head->nominal = nominal;
		head->count = count;
		head->currency = currecny;
		tail = head;
	}
	else
	{
		tail->next = new Money;
		tail->next->nominal = nominal;
		tail->next->count = count;
		tail->next->currency = currecny;

		Money* tmp = tail;
		tail = tail->next;
		tail->prev = tmp;
	}
}
FundList FundList::copy()
{
	FundList B;
	Money* tmp = head;
	while (tmp != nullptr) {
		B.push_back(tmp->nominal, tmp->currency.copy(), tmp->count);
		tmp = tmp->next;
	}
	return B;
}
void FundList::delete_element(Money* elem)
{
	R -= elem->count * elem->nominal;
	N--;
	if (elem == head)
	{
		head = head->next;

		elem->currency.delete_list();
		delete elem;

		if (head != nullptr)
			head->prev = nullptr;
	}
	else if (elem == tail)
	{
		tail = tail->prev;

		elem->currency.delete_list();
		delete elem;

		if (tail != nullptr) tail->next = nullptr;
	}
	else
	{
		Money* tmp1 = elem->prev,
			* tmp2 = elem->next;

		elem->currency.delete_list();
		delete elem;

		tmp2->prev = tmp1;
		tmp1->next = tmp2;
	}
}
void FundList::change_count(Money* elem, int k)
{
	elem->count += k;
	R += elem->nominal * k;
}

void FundList::out_list(fstream* f)
{
	Money* tmp = head;
	while (tmp != nullptr)
	{
		*f << "\tНоминал: " << tmp->nominal << endl;
		*f << "\tВалюта: "; tmp->currency.out_list(f);
		*f << "\n\tКоличество: " << tmp->count << "\n\t|\n\tV\n";
		tmp = tmp->next;
	}
	*f << "\tNULL\n";
}

void FundList::delete_list()
{
	Money* tmp;
	while (head != nullptr)
	{
		tmp = head;
		head = head->next;
		tmp->currency.delete_list();
		delete tmp;
	}
}