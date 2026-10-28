#include <iostream>

char* double_to_string(double x)
{
    int intPart = (int)(x);
    int fracPart = (int)((x - intPart) * 100);
    char* result = new char[intPart + 2 + 1];

    int i = 0;
    while (fracPart > 0) {
        result[i] = '0' + (fracPart % 10);
        fracPart /= 10;
        i++;
        std::cout << result[i] << std::endl;
    }
    result[i++] = '.';
    while (intPart > 0) {
        result[i] = '0' + (intPart % 10);
        intPart /= 10;
        i++;
        std::cout << result[i] << std::endl;
    }
    result[i--] = '\0';

    // reverse
    int j = 0;
    while (j < i) {
        char temp = result[j];
        result[j++] = result[i];
        result[i--] = temp;
    }

    return result;
}

int main()
{
    std::cout << double_to_string(1.134) << std::endl;
    return 0;
}