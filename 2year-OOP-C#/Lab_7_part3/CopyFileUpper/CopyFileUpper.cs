using System;
using System.IO;
public class CopyFileUpper
{
    public static void Main()
    {
        string sFrom, sTo;
        StreamReader srFrom;
        StreamWriter swTo;

        Console.Write("Enter input file name: ");
        sFrom = "C:\\Users\\DNS\\Desktop\\ПРОГА ВУЗ\\2 kurs\\ооп\\Lab7_part3\\CopyFileUpper\\";
        sFrom += Console.ReadLine();
        Console.Write("Enter output file name: ");
        sTo = "C:\\Users\\DNS\\Desktop\\ПРОГА ВУЗ\\2 kurs\\ооп\\Lab7_part3\\CopyFileUpper\\";
        sTo += Console.ReadLine();
        try
        {
            srFrom = new StreamReader(sFrom);
            swTo = new StreamWriter(sTo);
            string sBuffer;
            while (srFrom.Peek() != -1)
            {
                sBuffer = srFrom.ReadLine().ToUpper();
                swTo.WriteLine(sBuffer);
            }
            srFrom.Close();
            swTo.Close();
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine("Error: File was not found.");
        }
        catch (Exception)
        {
            Console.WriteLine("An error was detected.");
        }
    }
}
