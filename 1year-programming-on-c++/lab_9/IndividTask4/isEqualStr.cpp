#include "lib.h"
#include "StrList.h"

bool isEqualStr(Stroka* S1, Stroka* S2)
{
	Block* B1 = S1->data.get_head();
	Block* B2 = S2->data.get_head();

	while (1)
	{
		if (B1 == nullptr && B2 == nullptr) return 1;
		if ((B1 == nullptr && B2 != nullptr) || (B2 == nullptr && B1 != nullptr))
		{
			return 0;
		}

		for (unsigned i = 0; i < N; i++)
		{
			if (B1->str.pA[i] != B2->str.pA[i]) return 0;
			if ((B1->str.pA[i] == B1->str.Mark) || (B2->str.pA[i] == B2->str.Mark))
			{
				if ((B1->str.pA[i] == B1->str.Mark) && (B2->str.pA[i] == B2->str.Mark)) break;
				else return 0;
			}
		}

		B1 = B1->next;
		B2 = B2->next;
	}
	return 0;
}