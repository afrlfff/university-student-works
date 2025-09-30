#include "FundList.h"
#include "lib.h"

int GetMoney(FundList* myFund, fstream* fprotok)
{
	fstream f; f.open("fund.txt", ios::in);

	if (!f)
	{
		*fprotok << "Проблемы с открытием файла money.txt\n";
		f.close(); return 0;
	}

	char s, *strTmp = new char[BLOCK_SIZE];
	unsigned i;
	unsigned nominal, count;
	f << resetiosflags(ios::skipws);

	while (f)
	{
		f.get(); if (f.eof()) break;
		else
		{
			f.unget(); f >> nominal; f.get(); // get() считает пробел

			Stroka currency;
			do
			{
				i = 0;
				while (i < BLOCK_SIZE)
				{
					f.get(s);
					if (s == ',') break;
					f.unget(); f.get(strTmp[i]); i++;
				}
				if (i > 0) currency.push_back(strTmp, i);
			}
			while (s != ',');

			do { f.get(s); } while (s == ' ');
			f.unget(); f >> count; f.get(); // get() считает посл. символ строки

			myFund->push_back(nominal, currency, count);
		}
	}

	delete[] strTmp;
	f.close(); return 1;
}