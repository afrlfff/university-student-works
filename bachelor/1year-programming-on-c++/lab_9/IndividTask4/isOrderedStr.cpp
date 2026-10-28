#include "lib.h"
#include "StrList.h"
#include "func.h"

// проверяет, упорядочен ли набор строк S1, S2 по алфавиту (строго упорядочен)
bool isOrderedStr(Stroka* S1, Stroka* S2)
{
	Block* B1 = S1->data.get_head();
	Block* B2 = S2->data.get_head();

	while (1)
	{
		if (B2 == nullptr && B1 != nullptr) return 0;
		if (B1 == nullptr && B2 != nullptr) return 1;
		if (B2 == nullptr && B1 == nullptr) return 0;

		for (unsigned i = 0; i < N; i++)
		{
			if ((B1->str.pA[i] == B1->str.Mark) || (B2->str.pA[i] == B2->str.Mark))
			{
				if ((B1->str.pA[i] == B1->str.Mark) && (B2->str.pA[i] == B2->str.Mark)) return 0;
				else if ((B1->str.pA[i] == B1->str.Mark) && (B2->str.pA[i] != B2->str.Mark)) return 1;
				else return 0;
			}
			if ((B1->str.pA[i] != B2->str.pA[i]))
			{
				if (!isOrderedSymb(B1->str.pA[i], B2->str.pA[i]))
				{
					return 0;
				}
				else
				{
					return 1;
				}
			}
		}

		B1 = B1->next;
		B2 = B2->next;
	}
	return 1;
}