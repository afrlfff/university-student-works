#ifndef FUNC
#define FUNC

int GetData(fstream* f, StrList** A);
int SetData(StrList* A1, StrList* A2, StrList* A3);
bool isEqualStr(Stroka* S1, Stroka* S2);
bool isOrderedSymb(char c1, char c2);
bool isOrderedStr(Stroka* S1, Stroka* S2);
int Process(fstream* f, StrList A1, StrList A2, StrList A3);

#endif
