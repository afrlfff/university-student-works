#include "func.h"

bool operator == (Stroka a, Stroka b)
{
	StrBlock* tmp1 = a.get_head(),
		*tmp2 = b.get_head();

	while (tmp1 != nullptr && tmp2 != nullptr)
	{
		if (tmp1->str.L != tmp2->str.L) return 0;
		else
		{
			for (unsigned i = 0; i < tmp1->str.L; i++)
			{
				if (tmp1->str.pA[i] != tmp2->str.pA[i]) return 0;
			}
			tmp1 = tmp1->next;
			tmp2 = tmp2->next;
		}
	}
	if (tmp1 == nullptr && tmp2 == nullptr) return 1;
	return 0;
}
bool operator == (QueriesList a, QueriesList b)
{
	Query* qtmp1 = a.get_head(),
		* qtmp2 = b.get_head();

	while (qtmp1 != nullptr && qtmp2 != nullptr)
	{
		if ((qtmp1->money.nominal != qtmp2->money.nominal) ||
			(qtmp1->money.count != qtmp2->money.count)) {
			return 0;
		}

		qtmp1 = qtmp1->next;
		qtmp2 = qtmp2->next;
	}
	if (qtmp1 == nullptr && qtmp2 == nullptr) return 1;
	return 0;
}