#pragma once

#include "FundList.h"
#include "ClientsList.h"

int GetMoney(FundList* myFund, fstream* fprotok);
int GetClients(ClientsList* Clients, fstream* fprotok);
void Process(FundList* Fund, ClientsList* Clients, fstream* fprotok);
bool operator == (Stroka a,Stroka b);
bool operator == (QueriesList a, QueriesList b);