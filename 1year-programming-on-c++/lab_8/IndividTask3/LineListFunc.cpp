#include <iostream>
#include "LinesList.h"
using namespace std;

LinesList::LinesList()
{
	Size = 0;
	head = nullptr;
}
LinesList::~LinesList()
{

}
void LinesList::set_data(char* stroka, unsigned length)
{
	if (head == nullptr)
	{
		head = new Line;
		head->pStroka = stroka;
		head->L = length;
	}
	else
	{
		Line* currentLine = head;
		while (currentLine != nullptr)
		{
			currentLine = currentLine->pNext;
		}
		currentLine = new Line;
		currentLine->pStroka = stroka;
		currentLine->L = length;
	}
}
void LinesList::push_back(char* stroka, unsigned length)
{
	if (head == nullptr)
	{
		head = new Line;
		head->pStroka = stroka;
		head->L = length;
	}
	else
	{
		Line* currentLine = head;
		while (currentLine->pNext != nullptr)
		{
			currentLine = currentLine->pNext;
		}
		currentLine->pNext = new Line;
		currentLine->pStroka = stroka;
		currentLine->L = length;
	}
	Size++;
}
void LinesList::delete_element(char stroka)
{
	Line* element = head;
	while ((*element->pStroka != stroka) && (element != nullptr))
	{
		element = element->pNext;
	}

	if (element != nullptr)
	{
		// на этом моменте мы также знаем, что head != nullptr
		if (element == head)
		{
			head = element->pNext;
			delete element;
		}
		else
		{
			Line* previous = head;
			while (previous->pNext != element)
			{
				previous = previous->pNext;
			}
			previous->pNext = element->pNext;
			delete element;
		}
		Size--;
	}
}
void LinesList::out_list()
{
	if (head != nullptr)
	{
		cout << "Вывод элементов списка.\nРазмер: " << Size << " элементов.\n\n";
		Line* tmp = head;
		while (tmp != nullptr)
		{
			// out
			cout << tmp->pStroka << "\t-->\n";
			tmp = tmp->pNext;
		}
		cout << "END";
	}
}
void LinesList::delelte_list()
{
	Line* tmp = head;
	while (head != nullptr)
	{
		tmp = head;
		head = head->pNext;
		delete tmp;
	}
}
