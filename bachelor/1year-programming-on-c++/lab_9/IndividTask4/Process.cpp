#include "lib.h"
#include "StrList.h"
#include "func.h"


int Process(fstream* f, StrList A1, StrList A2, StrList A3)
{
	Stroka* Str1 = A1.get_head(); // указатель на головной элемент списка A1
	Stroka* Str2 = A2.get_head(); // указатель на головной элемент списка A2
	Stroka* Str3 = A3.get_head(); // указатель на головной элемент списка A3
	Stroka* tmp;
	int flag = 0;

	// S3 in (S1<->S2)

	if (Str3 == nullptr) flag = 1;
	else
	{
		while (1)
		{
			if (Str1 != nullptr && Str2 != nullptr)
			{
				if (isEqualStr(Str1, Str2))
				{
					if (Str1 != nullptr) Str1 = Str1->next;
					if (Str2 != nullptr) Str2 = Str2->next;
				}
				else if (isOrderedStr(Str1, Str2)) // если строка Str1 по алфавиту находится раньше, чем Str2
				{
					tmp = Str1;

					while (Str1 != nullptr)
					{
						Str1 = Str1->next;
						if ((Str1 == nullptr) ||
							(!isOrderedStr(Str1, Str2)))
							break;
					}

					// check if tmp in A3
					if (!isEqualStr(Str3, tmp)) flag = 0;
					else
					{
						if (Str3 == nullptr)
						{
							flag = 1; break;
						}
						else Str3 = Str3->next;
					}
				}
				else // если строка Str1 по алфавиту находится дальше, чем Str2
				{

					tmp = Str2;

					while (Str2 != nullptr)
					{
						Str2 = Str2->next;
						if ((Str2 == nullptr) || 
							(!isOrderedStr(Str2, Str1)))
							break;
					}

					// check if tmp in A3
					if (!isEqualStr(Str3, tmp)) flag = 0;
					else
					{
						if (Str3 == nullptr) 
						{
							flag = 1; break;
						}
						else Str3 = Str3->next;
					}
				}
			}
			else if ((Str1 != nullptr && Str2 == nullptr) || (Str1 == nullptr && Str2 != nullptr))
			{
				Stroka* tmp2;
				if (Str1 == nullptr) tmp2 = Str2;
				else tmp2 = Str1;

				while (1)
				{
					if (tmp2 == nullptr || Str3 == nullptr)
					{
						if (Str3 == nullptr) flag = 1;
						else flag = 0;
						break;
					}
					if (isEqualStr(tmp2, Str3))
					{
						if (tmp2 != nullptr) tmp2 = tmp2->next;
						if (Str3 != nullptr) Str3 = Str3->next;
					}
					else if (isOrderedStr(tmp2, Str3)) // если строка strTmp по алфавиту находится раньше, чем Str3
					{
						while (tmp2 != nullptr)
						{
							tmp2 = tmp2->next;
							if ((tmp2 == nullptr) ||
								(!isOrderedStr(tmp2, Str3)))
								break;
						}

						// check if current element in A3
						if ((tmp2 == nullptr) || (!isEqualStr(tmp2, Str3)))
						{
							flag = 0; break;
						}
						else
						{
							if (Str3 == nullptr)
							{
								flag = 1; break;
							}
							else Str3 = Str3->next;
						}
					}
					else // если строка strTmp по алфавиту находится дальше, чем Str3
					{
						flag = 0; break;
					}
				}
				break;
			}
			else
			{
				if (Str3 == nullptr) flag = 1;
				else flag = 0;
				break;
			}
		}
	}

	if (flag) *f << "Ответ: да\n";
	else *f << "Ответ: нет\n";

	return 0;
}