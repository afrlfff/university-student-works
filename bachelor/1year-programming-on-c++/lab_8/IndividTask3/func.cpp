#include "LinesList.h"
#include "func.h"
#include <iomanip>
using namespace std;

// List Functions

LinesList::LinesList()
{
	Size = 0;
	head = nullptr;
}
LinesList::~LinesList()
{
	delelte_list();
}
bool LinesList::str_equality(char* stroka1, char* stroka2, unsigned l1, unsigned l2)
{
	if (l1 == l2)
	{
		for (unsigned i = 0; i < l1; i++)
		{
			if (stroka1[i] != stroka2[i]) return false;
		}
		return true;
	}
	return false;
}
void LinesList::push_back(char* stroka, unsigned length)
{
	if (head == nullptr)
	{
		head = new Line;
		head->strl.pStroka = new char[length];
		for (unsigned i = 0; i < length; i++)
		{
			head->strl.pStroka[i] = stroka[i];
		}
		head->strl.L = length;
	}
	else
	{
		Line* currentLine = head;
		while (currentLine->pNext != nullptr)
		{
			currentLine = currentLine->pNext;
		}
		currentLine->pNext = new Line;
		currentLine->pNext->strl.pStroka = new char[length];
		for (unsigned i = 0; i < length; i++)
		{
			currentLine->pNext->strl.pStroka[i] = stroka[i];
		}
		currentLine->pNext->strl.L = length;
	}
	Size++;
}
void LinesList::delete_elements(char* stroka, unsigned l2)
{
	Line* current = head;

	while (1)
	{
		if (current == nullptr) break;

		if (str_equality(current->strl.pStroka, stroka, current->strl.L, l2))
		{
			if (current == head)
			{
				Line* tmp = current;
				current = current->pNext;
				head = current;
				delete tmp;
			}
			else
			{
				Line* previous = head;
				while (previous->pNext != current)
				{
					previous = previous->pNext;
				}
				previous->pNext = current->pNext;
				
				Line* tmp = current;
				current = current->pNext;
				delete tmp;
			}
			Size--;
		}
		else
		{
			current = current->pNext;
		}
	}
}
void LinesList::out_list(fstream* fout)
{
	if (head != nullptr)
	{
		cout << "Размер списка: " << Size << " элемента(-ов).\n\n";
		*fout << "Размер списка: " << Size << " элемента(-ов).\n\n";
		Line* tmp = head;
		while (tmp != nullptr)
		{
			// out
			if (tmp == head)
			{
				cout << "\t" << tmp->strl.pStroka << " --->\n";
				*fout << "\t\t" << tmp->strl.pStroka << " --->\n";
			}
			else
			{
				cout << "--->\t" << tmp->strl.pStroka << " --->\n";
				*fout << "--->\t" << tmp->strl.pStroka << " --->\n";
			}
			tmp = tmp->pNext;
		}
		cout << "--->\tNULL\n\n";
		*fout << "--->\tNULL\n\n";
	}
	else
	{
		cout << "\tNULL";
		*fout << "\t\tNULL";
	}
}
void LinesList::delelte_list()
{
	Line* tmp = head;
	while (head != nullptr)
	{
		tmp = head;
		head = head->pNext;
		delete[] tmp->strl.pStroka;
		delete tmp;
	}
}

// Other Functions

void OutError(fstream* fout, int error)
{
	switch (error)
	{
	case 11: // Output 1.1
		*fout << "ОШИБКА: не удалось открыть входной файл.\n";
	}
	fout->close();
}
int GetData(LinesList* Lines)
{
	fstream fin, fout;
	fout.open("out.txt", ios::out);
	fin.open("in.txt", ios::in);
	if (!fin.is_open()) { OutError(&fout, 11); fin.close(); return 0; }

	fin << resetiosflags(ios::skipws);
	char s;
	int tmp = 0;
	unsigned i, length = 0;
	char* stroka;


	while (1)
	{
		fin >> s;
		tmp++;

		if (s == '\n' && !(fin.eof()))
		{
			tmp--;
			fin.seekg(-(tmp + 2), ios::cur);
			length = tmp + 1; // для хранения '\0'
			char* stroka = new char[length];

			for (i = 0; i < (length - 1); i++)
			{
				fin >> stroka[i];
			}
			stroka[length - 1] = '\0'; // ! обязательно для символьного массива 
			fin >> s; // go to next line

			// set data
			if (length > 1) Lines->push_back(stroka, length);
			delete[] stroka;
			tmp = 0;
		}
		else if (fin.eof())
		{
			fin.clear();
			tmp--;
			fin.seekg(-tmp, ios::end);
			length = tmp + 1; // для хранения '\0'
			stroka = new char[length];

			for (i = 0; i < (length - 1); i++)
			{
				fin >> stroka[i];
			}
			stroka[length - 1] = '\0'; // ! обязательно для символьного массива 

			// set data
			if (length > 1) Lines->push_back(stroka, length);
			delete[] stroka;
			tmp = 0;
			break;
		}
	}
	fin.close(); fout.close();
	return 1;
}
int GetStrDel(char** strDel, unsigned* length)
{
	fstream fin, fout;
	fout.open("out.txt", ios::out);
	fin.open("strDel.txt", ios::in);
	if (!fin.is_open()) { OutError(&fout, 11); fin.close(); return 0; }

	fin << resetiosflags(ios::skipws);
	char s;
	unsigned tmp;

	tmp = 0;
	do
	{
		fin >> s;
		if (!fin.eof()) tmp++;
	} while (!fin.eof());

	if (tmp > 0)
	{
		fin.clear();
		fin.seekg(0, ios::beg);
		*strDel = new char[tmp + 1]; // '\0'
		for (unsigned i = 0; i < tmp; i++)
		{
			fin >> (*strDel)[i];
		}
		(*strDel)[tmp] = '\0';
		*length = tmp + 1;

		fin.close(); fout.close();
		return 1;
	}

	fin.close(); fout.close();
	return 0;
} 