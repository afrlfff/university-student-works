using System;
class Dividing
{
    static void Main(string[] args)
    {
        try
        {
            int i, j;
            string temp;
            Console.WriteLine("Enter first integer digit");
            temp = Console.ReadLine();
            i = int.Parse(temp);
            Console.WriteLine("Enter second integer digit");
            temp = Console.ReadLine();
            j = int.Parse(temp);
            int k;
            k = i / j;
            Console.WriteLine("{0}/{1} is {2}", i, j, k);
        }
        catch
        {
            Console.WriteLine("An error occurred due to incorrect initial values.");
        }
    }
}