#ifndef LINESLIST
#define LINESLIST

#include "Line.h"
#include <fstream>
using namespace std;

class LinesList
{
private:
	int Size;
	Line* head;

	bool str_equality(char* stroka1, char* stroka2, unsigned l1, unsigned l2);
public:
	LinesList();
	~LinesList();

	void push_back(char* stroka, unsigned L);
	void delete_elements(char* stroka, unsigned l2);
	void out_list(fstream* fout);
	void delelte_list();
};

#endif 