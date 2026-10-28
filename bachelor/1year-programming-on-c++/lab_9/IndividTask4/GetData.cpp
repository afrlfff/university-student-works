#include "lib.h"
#include "StrList.h"

int GetData(fstream* f, StrList** A)
{
	*f << resetiosflags(ios::skipws);

	unsigned size;
	char* stroka = new char[N];
	bool flag; // не пустой ли BlockList

	char s; *f >> s;
	if (f->eof()) return 0;
	else f->unget();

	while (!f->eof())
	{
		BlockList B;
		size = 0;
		flag = false;

		while (1)
		{
			*f >> stroka[size]; size++;
			if (stroka[size - 1] == '\n')
			{
				// (size - 1) т.к. послед. элемент = '\n'
				B.push(stroka, size - 1); flag = true;
				break;
			}
			else if (f->eof())
			{
				// (size - 1) т.к. послед. элемент - мусор
				B.push(stroka, size - 1); flag = true;
				break;
			}
			else if (size == N)
			{
				B.push(stroka, size);
				size = 0; flag = true;
			}
		}
		if (flag) (**A).push(B);
	}

	delete[] stroka;
	return 0;
}