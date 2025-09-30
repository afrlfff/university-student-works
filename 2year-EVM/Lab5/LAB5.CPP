#include <dos.h>
#include <conio.h>
#include <stdio.h>

// Объявление обработчика прерывания клавиатуры
void interrupt (*prevKeyboardInterrupt)(...);

// Функция обработки прерывания клавиатуры
void interrupt myKeyboardInterrupt(...)
{
    // Передать управление стандартной подпрограмме обработки прерывания клавиатуры
    (*prevKeyboardInterrupt)();
}

int main()
{
    // Установка собственного обработчика прерывания клавиатуры
    prevKeyboardInterrupt = getvect(0x09); // Получаем адрес старого обработчика
    setvect(0x09, myKeyboardInterrupt); // Устанавливаем адрес нового обработчика
    
    // Восстановление стандартного обработчика прерывания клавиатуры
    setvect(0x09, prevKeyboardInterrupt);
    
    getch();
    return 0;
}