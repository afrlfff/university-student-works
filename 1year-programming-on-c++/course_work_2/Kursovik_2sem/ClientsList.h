#pragma once

#include "lib.h"
#include "Client.h"

class ClientsList
{
	Client* head;
	Client* tail;
public:
	unsigned N; // кол-во клиентов
	unsigned AllQueriesCount; // общее число запросов

	ClientsList();
	Client* get_head();
	Client* get_tail();
	ClientsList copy();
	void push_back(Stroka Name, Stroka Adress, QueriesList Query);
	void refresh_data();
	void delete_element(Client* elem);
	void out_list(fstream* f);
	void delete_list();
};
