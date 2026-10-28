using System;

class MatrixMultiply
{
    public static int[,] Result(int[,] a, int[,] b, out bool flag)
    {
        int[,] c = new int[2, 2];
        flag = true;
        
        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                try
                {
                    checked
                    {
                        c[i, j] = a[i, 0] * b[0, j] + a[i, 1] * b[1, j];
                    }

                }
                catch (OverflowException)
                {
                    c[i, j] = int.MaxValue;
                    Console.WriteLine("digit out of range was expected by calculating result Matrix");
                    flag = false;
                    return c;
                }
            }
        }

        return c;
    }
   public static void Main(string[] args)
   {
        int[,] a = new int[2, 2];
        int[,] b = new int[2, 2];

        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                Console.Write("Введите элемент a{0}{1}: ", i + 1, j + 1);
                while (true)
                {
                    try
                    {
                        a[i, j] = int.Parse(Console.ReadLine());
                        break;
                    }
                    catch (Exception)
                    {
                        Console.Write("Некорректный номер. Попробуйте ещё раз: ");
                    }
                }
            }
        }

        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                Console.Write("Введите элемент b{0}{1}: ", i + 1, j + 1);
                while (true)
                {
                    try
                    {
                        b[i, j] = Int32.Parse(Console.ReadLine());
                        break;
                    }
                    catch (Exception)
                    {
                        Console.Write("Некорректный номер. Попробуйте ещё раз: ");
                    }
                }
            }
        }

        int[,] c = new int[2, 2];
        bool flag;

        c = Result(a, b, out flag);
        if (flag)
        {
            Console.WriteLine("Результат перемножения: ");
            for (int i = 0; i < 2; i++)
            {
                Console.Write("\t");
                for (int j = 0; j < 2; j++)
                {
                    Console.Write("{0} ", c[i, j]);
                }
                Console.WriteLine();
            }
        }
    }
}

