#include "lib.h"
#include "QueriesList.h"

QueriesList::QueriesList()
{
	head = nullptr;
	tail = nullptr;
	N = 0;
	queriesCount = 0;
}
Query* QueriesList::get_head()
{
	return head;
}
Query* QueriesList::get_tail()
{
	return tail;
}
void QueriesList::push_back(unsigned nominal, Stroka currecny, unsigned count)
{
	queriesCount += count;
	N ++;
	if (head == nullptr)
	{
		head = new Query;
		head->money.nominal = nominal;
		head->money.count = count;
		head->money.currency = currecny;
		tail = head;
	}
	else
	{
		tail->next = new Query;
		tail->next->money.nominal = nominal;
		tail->next->money.count = count;
		tail->next->money.currency = currecny;

		Query* tmp = tail;
		tail = tail->next;
		tail->prev = tmp;
	}
}
void QueriesList::change_count(Query* elem, int k) {
	elem->money.count += k;
	queriesCount += k;
}
QueriesList QueriesList::copy()
{
	QueriesList B;
	Query* tmp = head;
	while (tmp != nullptr) {
		B.push_back(tmp->money.nominal, tmp->money.currency.copy(), tmp->money.count);
		tmp = tmp->next;
	}
	return B;
}
void QueriesList::delete_element(Query* elem)
{
	N--;
	queriesCount -= elem->money.count;
	if (elem == head)
	{
		head = head->next;

		elem->money.currency.delete_list();
		delete elem;

		if (head != nullptr)
			head->prev = nullptr;
	}
	else if (elem == tail)
	{
		tail = tail->prev;

		elem->money.currency.delete_list();
		delete elem;

		if (tail != nullptr) tail->next = nullptr;
	}
	else
	{
		Query *tmp1 = elem->prev,
			  *tmp2 = elem->next;

		elem->money.currency.delete_list();
		delete elem;

		tmp2->prev = tmp1;
		tmp1->next = tmp2;
	}
}
void QueriesList::out_list(fstream* f)
{
	Query* tmp = head;
	while (tmp != nullptr)
	{
		*f << "\t\tНоминал: " << tmp->money.nominal << endl;
		*f << "\t\tВалюта: "; tmp->money.currency.out_list(f);
		*f << "\n\t\tКоличество: " << tmp->money.count << "\n\t\t|\n\t\tV\n";
		tmp = tmp->next;
	}
	*f << "\t\tNULL\n";
}

void QueriesList::delete_list()
{
	Query* tmp;
	while (head != nullptr)
	{
		tmp = head;
		head = head->next;
		tmp->money.currency.delete_list();
		delete tmp;
	}
}