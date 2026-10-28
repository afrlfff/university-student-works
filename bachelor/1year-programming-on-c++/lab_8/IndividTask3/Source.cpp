#include <iostream>
#include <fstream>
#include "LinesList.h"
#include "func.h"

using namespace std;

int main()
{
	setlocale(LC_ALL, "ru");
	fstream fout;
	char* strDel = nullptr;
	unsigned length = 0;
	LinesList Lines;

	if (GetData(&Lines) && GetStrDel(&strDel, &length))
	{
		fout.open("out.txt", ios::out);
		fout << "Фролов Алексндр 2302\n\nСчитанные элементы:\n";
		Lines.out_list(&fout);

		Lines.delete_elements(strDel, length);
		delete[] strDel;

		fout << "Результат работы программы:\n";
		Lines.out_list(&fout);
	}
	return 0;
}