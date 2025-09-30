#include "ClientsList.h"

ClientsList::ClientsList()
{
	head = nullptr;
	tail = nullptr;
	N = 0;
	AllQueriesCount = 0;
}
Client* ClientsList::get_head()
{
	return head;
}
Client* ClientsList::get_tail()
{
	return tail;
}
void ClientsList::push_back(Stroka Name, Stroka Adress, QueriesList Query)
{
	N++;
	AllQueriesCount += Query.queriesCount;
	if (head == nullptr)
	{
		head = new Client;
		head->Name = Name;
		head->Adress = Adress;
		head->Queries = Query;
		tail = head;
	}
	else
	{
		tail->next = new Client;
		tail->next->Name = Name;
		tail->next->Adress = Adress;
		tail->next->Queries = Query;

		Client* tmp = tail;
		tail = tail->next;
		tail->prev = tmp;
	}
}
void ClientsList::refresh_data()
{
	Client* ctmp = head, *ctmp2;
	Query* qtmp, *qtmp2;
	bool flag1, flag2;
	while (ctmp != nullptr)
	{
		flag2 = false;
		qtmp = ctmp->Queries.get_head();
		while (qtmp != nullptr)
		{
			flag1 = false;
			if (qtmp->money.count == 0) {
				qtmp2 = qtmp;
				qtmp = qtmp->next; flag1 = true;
				ctmp->Queries.delete_element(qtmp2);
			}
			if (qtmp != nullptr && !flag1)
				qtmp = qtmp->next;
		}

		if (ctmp->Queries.N == 0) {
			ctmp2 = ctmp;
			ctmp = ctmp->next; flag2 = true;
			delete_element(ctmp2);
		}

		if (ctmp != nullptr && !flag2)
			ctmp = ctmp->next;
	}
}
ClientsList ClientsList::copy()
{
	ClientsList B;
	Client* tmp = head;
	while (tmp != nullptr) {
		B.push_back(tmp->Name.copy(), tmp->Adress.copy(), tmp->Queries.copy());
		tmp = tmp->next;
	}
	return B;
}
void ClientsList::delete_element(Client* elem)
{
	AllQueriesCount -= elem->Queries.queriesCount;
	N--;
	if (elem == head)
	{
		head = head->next;

		elem->Name.delete_list();
		elem->Adress.delete_list();
		elem->Queries.delete_list();
		delete elem;

		if (head != nullptr)
			head->prev = nullptr;
	}
	else if (elem == tail)
	{
		tail = tail->prev;

		elem->Name.delete_list();
		elem->Adress.delete_list();
		elem->Queries.delete_list();
		delete elem;

		if (tail != nullptr) tail->next = nullptr;
	}
	else
	{
		Client *tmp1 = elem->prev,
			*tmp2 = elem->next;

		elem->Name.delete_list();
		elem->Adress.delete_list();
		elem->Queries.delete_list();
		delete elem;

		tmp2->prev = tmp1;
		tmp1->next = tmp2;
	}
}
void ClientsList::out_list(fstream* f)
{
	Client* tmp = head;
	while (tmp != nullptr)
	{
		*f << "\tНаименование: "; tmp->Name.out_list(f);
		*f << "\n\tАдресс: "; tmp->Adress.out_list(f);
		*f << "\n\tЗапросы(" << tmp->Queries.queriesCount << " шт):\n"; tmp->Queries.out_list(f);
		*f << "\t|\n\tV\n";
		tmp = tmp->next;
	}
	*f << "\tNULL\n";
}
void ClientsList::delete_list()
{
	Client* tmp;

	while (head != nullptr)
	{
		tmp = head;
		head = head->next;

		tmp->Name.delete_list();
		tmp->Adress.delete_list();
		tmp->Queries.delete_list();
		delete tmp;
	}
}