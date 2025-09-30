#include "lib.h"
#include "StrList.h"
#include "func.h"


int main()
{
	setlocale(LC_ALL, "ru");
	fstream fout;

	StrList A1, A2, A3;
	if (SetData(&A1, &A2, &A3))
	{
		fout.open("out.txt", ios::out);
		fout << "Фролов Александр 2302.\n\n";
		fout << "Считанные элементы из файла in1.txt:\n";
		A1.out_list(&fout);
		fout << "Считанные элементы из файла in2.txt:\n";
		A2.out_list(&fout);
		fout << "Считанные элементы из файла in3.txt:\n";
		A3.out_list(&fout);

		Process(&fout, A1, A2, A3);
	}

	A1.delete_list();
	A2.delete_list();
	A3.delete_list();
	fout.close();
	return 0;
}