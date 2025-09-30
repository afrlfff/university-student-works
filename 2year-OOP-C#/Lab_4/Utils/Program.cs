using System;
using System.Collections.Specialized;
using System.Security.Cryptography.X509Certificates;

class Utils
{
    public static int Greater(int a, int b)
    {
        return a > b ? a : b;
    }
    public static void Swap(ref int a, ref int b)
    {
        int temp = a;
        a = b;
        b = temp;
    }
    public static bool Factorial(ref int n, out int answer)
    {
        try
        {
            checked
            {
                if (n == 0)
                {
                    answer = 1;
                    return true;
                }
                if (n < 0)
                {
                    throw new ArgumentOutOfRangeException("digit is out of range.\n");
                }
                answer = n;
                for (int i = 2; i < n; i++) answer *= i;

                return true;
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Вызывана ошибка: {ex.Message}");
            answer = 0;
            return false;
        }
        
    }
    public static int RecursiveFactorial(int n)
    {
        try
        {
            checked
            {
                if (n < 0)
                {
                    throw new ArgumentOutOfRangeException();
                }
                if (n == 1) return 1;
                if (n == 0) return 1;
                return n * RecursiveFactorial(n - 1);
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Вызывана ошибка: {ex.Message}");
            return -1;
        }
    }
}
class Test
{
    public static void Main(string[] args)
    {
        try
        {
            int x, y, greater, f1, f2;
            string line;
            Console.Write("Введите первое число: ");
            line = Console.ReadLine();
            x = int.Parse(line);
            Console.Write("Введите второе число: ");
            line = Console.ReadLine();
            y = int.Parse(line);
            Console.WriteLine("Введенные вами числа: {0}, {1}", x, y);
            greater = Utils.Greater(x, y);
            Console.WriteLine("Максимальное число: {0}", greater);
            Utils.Swap(ref x, ref y);
            Console.WriteLine("Результат после функции Swap(): {0}, {1}", x, y);
            if (Utils.Factorial(ref x, out f1))
            {
                Console.WriteLine("Факториал числа {0} был посчитан и равен: {1}.\n", x, f1);
            }
            else
            {
                Console.WriteLine("Факториал числа {0} не был посчитан.\n", x);
            }
            if (Utils.Factorial(ref y, out f2))
            {
                Console.WriteLine("Факториал числа {0} был посчитан и равен: {1}.\n", y, f2);
            }
            else
            {
                Console.WriteLine("Факториал числа {0} не был посчитан.\n", y);
            }
            if (Utils.RecursiveFactorial(x) < 0)
            {
                Console.WriteLine("Факториал числа {0} не был посчитан рекурсивно.\n", x);
            }
            else
            {
                Console.WriteLine("Факториал числа {0}, посчитанный рекурсивно: {1}\n", x, Utils.RecursiveFactorial(x));
            }
            if (Utils.RecursiveFactorial(y) < 0)
            {
                Console.WriteLine("Факториал числа {0} не был посчитан рекурсивно.\n", y);
            }
            else
            {
                Console.WriteLine("Факториал числа {0}, посчитанный рекурсивно: {1}\n", y, Utils.RecursiveFactorial(y));
            }
        }
        catch(Exception)
        {
            Console.WriteLine("Incorrect digit was expected.\n");
        }
    }
}