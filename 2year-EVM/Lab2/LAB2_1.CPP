#include <stdio.h>
#include <conio.h>
#include <dos.h>

const char MY_COLORS[16][15] = {
	"BLACK",
	"BLUE",
	"GREEN",
	"CYAN",
	"RED",
	"MARGENTA",
	"BROWN",
	"LIGHTGRAY",
	"DARKGRAY",
	"LIGHTBLUE",
	"LIGHTGREEN",
	"LIGHTCYAN",
	"LIGHTRED",
	"LIGHTMERGENTA",
	"YELLOW",
	"WHITE"
};

const int X1 = 10;
const int Y1 = 15;
const int X2 = 70;
const int Y2 = 20;

const float T = 0.7f;
const int S = 3;

int main()
{
	window(X1, Y1, X2, Y2);

	for (int i = 0; i < 16; i++) {
		for (int j = 0; j < 16; j++) {
			textbackground(i);
			textcolor(j);

			cprintf("Background: %s, Text: %s", MY_COLORS[i], MY_COLORS[j]);

			delay(T * 1000);
			clrscr();
		}
	}
	return 0;
}