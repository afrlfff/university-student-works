#pragma once

#include "Stroka.h"

struct Money
{
	unsigned nominal = 0;
	Stroka currency; // ������
	unsigned count = 0; // ���-�� ����� ������� ��������

	Money* next = nullptr;
	Money* prev = nullptr;
};
