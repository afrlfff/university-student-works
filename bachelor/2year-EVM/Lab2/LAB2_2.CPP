#include <stdio.h>
#include <conio.h>
#include <dos.h>

// START CONSTANTS
enum Direction { ENTIRE, UP, DOWN };
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

const Direction dir = UP;

// END CONSTANTS

void scroll(char l_row, char l_col, char r_row, char r_col, char attr)
{
	union REGS r;
	if (dir == DOWN)
		r.h.ah = 6;
	else
		r.h.ah = 7;

	r.h.al = 1;
	r.h.ch = l_row;
	r.h.cl = l_col;
	r.h.dh = r_row;
	r.h.dl = r_col;

	r.h.bh = attr;
	int86(0x10, &r, &r);
}

int main()
{
	window(X1, Y1, X2, Y2);

	for(int i = 0; i < 16; i++) {
		for(int j = 0; j < 16; j++) {
			textbackground(i);
			textcolor(j);
			if (dir == UP)
				cprintf("\rBackground: %s, Text: %s", MY_COLORS[i], MY_COLORS[j]);
			else
				cprintf("\n\rBackground: %s, Text: %s", MY_COLORS[i], MY_COLORS[j]);
			delay(T*1000);

			if (dir == UP)
				scroll(Y1 - 1, X1 - 1, Y2 - 1, X2 - 1, (i * 16 | j));
			else
				scroll(0, 0, 256, 256, (i * 16 | j));
		}
	}

	clrscr();
	return 0;
}