#include <stdio.h>
#include <conio.h>
#include <math.h>
#include <graphics.h>

double pi = 3.14159265358979323846;

// X area
    const double START_X = 1 * pi;  // can be changed
    const double END_X = 11 * pi;  // can be changed
// count of points on the graph
    const int COUNT_OF_POINTS = 101; // can be changed
// Offset of the graphfrom the edges of the screen 
    const int HORIZONTAL_OFFSET = 0;  // can be changed
    const int VERTICAL_OFFSET = 100;  // can be changed
// coefficients to convert X and Y values to graph point
    int GRAPH_START_X = HORIZONTAL_OFFSET;
    int GRAPH_START_Y = VERTICAL_OFFSET;
    int GRAPH_END_X; // will be calculated after graph initialization
    int GRAPH_END_Y; // will be calculated after graph initialization

double calculate_function(double x) {
    return pow(sin(x / 4), 2) - sqrt(x);
}

double my_abs(double x) {
    if (x < 0) return -x;
    return x;
}

int xToGraphPoint(double x, double maxX, double minX, int graphLeftOffset = 0) {
    double coeff = my_abs(x - minX) / my_abs(maxX - minX);
    int graphStartX = GRAPH_START_X + graphLeftOffset;
    return (int)(graphStartX + coeff * (GRAPH_END_X - graphStartX));
}
int yToGraphPoint(double y, double maxY, double minY) {
    double coeff = my_abs(y - minY) / my_abs(maxY - minY);
    return (int)(GRAPH_END_Y - coeff * (GRAPH_END_Y - GRAPH_START_Y));
}

void initAxes(double minX, double maxX, double minY, double maxY, int& graphLeftOffset) {
    // constants
    setcolor(WHITE);
    const int Y_AXIS_OFFSET = 40; // Y axis left edge offset
    const int COUNT_OF_TICKS = (int)(END_X / START_X); // count of ticks on the X axis
    const int STEP = (GRAPH_END_X - GRAPH_START_X - Y_AXIS_OFFSET) / COUNT_OF_TICKS; // distance between two ticks

    // calculating graphLeftOffset
    double coeff = my_abs(minX - 0) / my_abs(maxX - minX);
    graphLeftOffset = (int)((GRAPH_END_X - GRAPH_START_X) * coeff);

    // X and Y axis
    line(GRAPH_START_X + Y_AXIS_OFFSET, (GRAPH_END_Y + GRAPH_START_Y) / 2,
        GRAPH_END_X, (GRAPH_END_Y + GRAPH_START_Y) / 2);
    line(GRAPH_START_X + Y_AXIS_OFFSET, GRAPH_START_Y,
        GRAPH_START_X + Y_AXIS_OFFSET, GRAPH_END_Y);

    // Coordinates of Y axis
    char buffer[20];
    sprintf(buffer, "%.2f", maxY);
    outtextxy(GRAPH_START_X, GRAPH_START_Y + 5, buffer);
    sprintf(buffer, "%.2f", minY);
    outtextxy(GRAPH_START_X, GRAPH_END_Y - 5, buffer);
    sprintf(buffer, "%.2f", (maxY + minY) / 2);
    outtextxy(GRAPH_START_X, (GRAPH_END_Y + GRAPH_START_Y) / 2, buffer);

    // Coordinates of X axis
    const int numberOffset = 30;
    outtextxy(Y_AXIS_OFFSET + 0 * STEP, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "0");
    outtextxy(Y_AXIS_OFFSET + 1 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "1pi");
    outtextxy(Y_AXIS_OFFSET + 2 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "2pi");
    outtextxy(Y_AXIS_OFFSET + 3 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "3pi");
    outtextxy(Y_AXIS_OFFSET + 4 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "4pi");
    outtextxy(Y_AXIS_OFFSET + 5 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "5pi");
    outtextxy(Y_AXIS_OFFSET + 6 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "6pi");
    outtextxy(Y_AXIS_OFFSET + 7 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "7pi");
    outtextxy(Y_AXIS_OFFSET + 8 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "8pi");
    outtextxy(Y_AXIS_OFFSET + 9 * STEP - numberOffset, (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "9pi");
    outtextxy(Y_AXIS_OFFSET + 10 * STEP - (numberOffset + 20), (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "10pi");
    //outtextxy(Y_AXIS_OFFSET + 11 * STEP - (numberOffset + 20), (GRAPH_END_Y + GRAPH_START_Y) / 2 + 5, "11pi");
}


int main() {
    // distance between points on X axis
    // (COUNT_OF_POINTS - 1) because we need END_X being included  
    const double STEP = (END_X - START_X) / (COUNT_OF_POINTS - 1);

    // X and Y values on the graph
    double *arrX = new double[COUNT_OF_POINTS];
    double *arrY = new double[COUNT_OF_POINTS];
    // X and Y area
    double maxX = END_X, minX = START_X;
    double maxY = -1e9, minY = 1e9;

    int i;
    // calculating X and Y values
    for (i = 0; i < COUNT_OF_POINTS; i++) {
        arrX[i] = START_X + i * STEP;
        arrY[i] = calculate_function(arrX[i]);

        if (arrY[i] > maxY) maxY = arrY[i];
        if (arrY[i] < minY) minY = arrY[i];
    }


    // initializing graphics
    clrscr();
    int gd = DETECT;
    int gm;
    initgraph(&gd, &gm, "..\\BGI");
    if (graphresult() < 0)
    {
        cprintf("\nGRAPHICS INITIALIZATION FAILED!\n");
        cprintf("ENTER ANY KEY...");
        getch();
        return 0;
    }

    // PLOTTING

    GRAPH_END_X = (getmaxx() - HORIZONTAL_OFFSET);
    GRAPH_END_Y = (getmaxy() - VERTICAL_OFFSET);
    setbkcolor(BLACK);
    int graph_left_offset;
    initAxes(minX, maxX, minY, maxY, graph_left_offset);

    setcolor(LIGHTGREEN);
    int x1, y1, x2, y2;
    for (i = 0; i < (COUNT_OF_POINTS - 1); i++) {
        // line(x1, y1, x2, y2) - takes coordinate of two points
        // but considering X and Y axis are inverted on the screen representation
        // I set Y value to X parameter and X value to Y parameter

        // screen representation
        //                          Y
        //   -------------------------------------------------->
        //   | (0, 0)                           (getmaxx(), 0)
        //   |
        // X |
        //   |
        //   | (0, getmaxy())           (getmaxx(), getmaxy())
        //   v

        
        x1 = xToGraphPoint(arrX[i], maxX, minX, graph_left_offset);
        y1 = yToGraphPoint(arrY[i], maxY, minY);
        x2 = xToGraphPoint(arrX[i+1], maxX, minX, graph_left_offset);
        y2 = yToGraphPoint(arrY[i+1], maxY, minY);

        line(x1, y1, x2, y2);
    }

    // MAX VALUE OUTPUT
    setcolor(CYAN);
    char buffer[20];
    sprintf(buffer, "Max value = %.2f", maxY);
    outtextxy((GRAPH_END_X + GRAPH_START_X) / 2 + 10, GRAPH_START_Y + 10, buffer);


    delete[] arrX;
    delete[] arrY;

    getch();
    closegraph();

    return 1;
}
