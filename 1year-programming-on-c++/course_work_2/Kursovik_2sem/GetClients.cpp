#include "lib.h"
#include "ClientsList.h"

int GetClients(ClientsList* Clients, fstream* fprotok)
{
	fstream f1; f1.open("clients.txt", ios::in);
	fstream f2; f2.open("queries.txt", ios::in);

	if (!f1)
	{
		*fprotok << "Проблемы с открытием файла clients.txt\n";
		f1.close(); f2.close(); return 0;
	}
	if (!f2)
	{
		*fprotok << "Проблемы с открытием файла queries.txt\n";
		f1.close(); f2.close(); return 0;
	}

	f1 << resetiosflags(ios::skipws);
	f2 << resetiosflags(ios::skipws);
	char s, *strTmp = new char[BLOCK_SIZE];
	unsigned i, nominal, count;

	while (f1)
	{
		f1.get(s); if (!f1) break;
		else
		{
			f1.unget();

			// Get Name
			Stroka Name;
			do
			{
				i = 0;
				while (i < BLOCK_SIZE)
				{
					f1.get(s);
					if (s == ';') break;
					f1.unget(); f1.get(strTmp[i]); i++;
				}
				if (i > 0) Name.push_back(strTmp, i);
			} while (s != ';');

			do { f1.get(s); } while (s == ' '); f1.unget();

			// Get Adress
			Stroka Adress;
			do
			{
				i = 0;
				while (i < BLOCK_SIZE)
				{
					f1.get(s);
					if (s == '\n' || !f1) break;
					f1.unget(); f1.get(strTmp[i]); i++;
				}
				if (i > 0) Adress.push_back(strTmp, i);
			} while (s != '\n' && f1);

			// Get Query
			QueriesList Query;
			s = ' ';
			while(s != '\n' && f2)
			{
				Stroka currency;

				do { f2.get(s); } while (s == ' ');
				f2.unget(); f2 >> nominal; f2.get(); // get() считает пробел
				do
				{
					i = 0;
					while (i < BLOCK_SIZE)
					{
						f2.get(s);
						if (s == ',') break;
						f2.unget(); f2.get(strTmp[i]); i++;
					}
					if (i > 0) currency.push_back(strTmp, i);
				} while (s != ',');

				do { f2.get(s); } while (s == ' ');
				f2.unget(); f2 >> count; f2.get(s); // get(s) считает последний символ

				Query.push_back(nominal, currency, count);
			}

			Clients->push_back(Name, Adress, Query);
		}
	}

	delete[] strTmp;
	f1.close(); f2.close(); return 1;
}