#include <stdio.h>
#include <conio.h>
#include <dos.h>


// Individual values
const int X1 = 10;
const int Y1 = 15;
const int X2 = 70;
const int Y2 = 20;
// ASII codes of keys which are used to move the character '*'
const int moveUp = 72; // up arrow
const int moveDown = 80; // down arrow
const int moveLeft = 75; // left arrow
const int moveRight = 77; // right arrow

// limits of the character movement
const int sizeX = X2 - X1 + 1;
const int sizeY = Y2 - Y1 + 1;

const float DELAY_FOR_MOVING = 0.1f; // in seconds

int getch_replacement() 
{
    union REGS regs;
    regs.h.ah = 0x01;
    int86(0x21, &regs, &regs);
    return regs.h.al;
}

void updatePosition(int x, int y){
    // clear screen to update character position
    clrscr();

    // moves cursor to poisition (x, y)
    gotoxy(x, y);

    // to show current position
    printf("*\n");
}

int main()
{
    // exit flag
    int exit = 0;

    // current charcter position
    int x, y;
    // set current character position to the center of screen 
    x = (X2 - X1) / 2;
    y = (Y2 - Y1) / 2;

    // to keep the ASII code of character
    int c = 0;

    // Initialize window and colors
    window(X1, Y1, X2, Y2);
    textbackground(BLUE);
    textcolor(WHITE);

    while (exit == 0)
    {
        updatePosition(x, y);
        
        // get current character
        c = getch_replacement();
    
        // ПОСТОЯННОЕ ДВИЖЕНИЕ
        switch (c)
        {
        case moveUp:
            while (y > 1)
            {
                y -= 1;
                delay(DELAY_FOR_MOVING * 1000);
                updatePosition(x, y);
            }
            break;

        case moveDown:
            while (y < sizeY)
            {
                y += 1;
                delay(DELAY_FOR_MOVING * 1000);
                updatePosition(x, y);
            }
            break;

        case moveLeft:
            while ((x - 1) > 1)
            {
                x -= 1;
                delay(DELAY_FOR_MOVING * 1000);
                updatePosition(x, y);
            }
            break;
            
        case moveRight:
            while ((x + 1) < sizeX)
            {
                x += 1;
                delay(DELAY_FOR_MOVING * 1000);
                updatePosition(x, y);
            }
            break;
        case 27:
            // if user press 'esc' key
            exit = 1;
            break;
        default:
            break;
        }
    }

    return 0;
}
