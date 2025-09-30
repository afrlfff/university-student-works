#include "lib.h"
#include "StrList.h"
#include "func.h"

int SetData(StrList* A1, StrList* A2, StrList* A3)
{
	fstream f1, f2, f3, fout;
	f1.open("in1.txt", ios::in);
	f2.open("in2.txt", ios::in);
	f3.open("in3.txt", ios::in);
	fout.open("out.txt", ios::out);

	if ((!f1.is_open()) || (!f2.is_open()) || (!f3.is_open()))
	{
		fout << "Проблемы с открытием входного файла.\n";
		f1.close(); f2.close(); f3.close(); fout.close();
		return 0;
	}

	GetData(&f1, &A1);
	GetData(&f2, &A2);
	GetData(&f3, &A3);

	f1.close(); f2.close(); f3.close(); fout.close();
	return 1;
}