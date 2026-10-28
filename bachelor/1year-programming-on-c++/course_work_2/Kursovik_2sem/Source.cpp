#include "lib.h"
#include "FundList.h"
#include "ClientsList.h"
#include "func.h"

int main()
{
	setlocale(LC_ALL, "ru");

	FundList Fund;
	ClientsList Clients;
	fstream fprotok; fprotok.open("protokol.txt", ios::out);
	fprotok << "ÏÐÎÒÎÊÎË Ê ÊÓÐÑÎÂÎÉ ÐÀÁÎÒÅ.\n\n";

	if (GetMoney(&Fund, &fprotok) && GetClients(&Clients, &fprotok))
	{
		fprotok	<< "Ñ÷èòàííûé ôîíä îðãàíèçàöèè(R = " << Fund.R << " äåí. åä.):\n";
		Fund.out_list(&fprotok);
		fprotok << "\nÑ÷èòàííûå êëèåíòû(" << Clients.N << " êë.):\n";
		Clients.out_list(&fprotok);
		
		Process(&Fund, &Clients, &fprotok);
	}

	Fund.delete_list();
	Clients.delete_list();
	fprotok.close(); return 0;
}

