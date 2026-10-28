using System;
using System.IO;

class FileDetails
{
    public static void Main(string[] args)
    {
        try
        {
            if (args.Length == 0)
            {
                throw new IndexOutOfRangeException("Error: No arguments was given in Main()");
            }

            string fileName = args[0];
            Console.WriteLine("Длина массива args: {0}", args.Length);
            Console.Write("Переданные аргументы в Main(): ");
            foreach (string arg in args)
            {
                Console.Write(arg + " ");
            }
            Console.WriteLine();

            FileStream stream = new FileStream(fileName, FileMode.Open);
            StreamReader reader = new StreamReader(stream);

            long fileLength = 0;
            while (reader.Peek() != -1)
            {
                reader.Read();
                fileLength++;
            }
            reader.DiscardBufferedData();
            reader.BaseStream.Seek(0, SeekOrigin.Begin);

            char[] contents = new char[fileLength];
            for(int i = 0; i < fileLength; i++)
            {
                contents[i] = (char)reader.Read();
            }
            Console.Write("Считанные данные из файла: ");

            /*
                foreach (char content in contents)
                {
                    Console.Write(content);
                }
                Console.WriteLine();
            */

            Summarize(contents);

            reader.Close();
            stream.Close();
        }
        catch(IndexOutOfRangeException)
        {
            Console.WriteLine("index out of range error.");
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine("Error: File was not found");
        }
        catch(Exception)
        {
            Console.WriteLine("An error was expected.");
        }
    }
    public static void Summarize(char[] contents)
    {
        int strCount = 0,
            simbCount = 0,
            vowelCount = 0,
            novowelCount = 0;

        foreach (char content in contents)
        {
            if (content != '\n' && content != '\r')
                simbCount++;
            if (content == '\n')
                strCount++;
            else if (content != '\r')
            {
                if ("АЕЁИОУЫЭЮЯаеёиоуыэюя".IndexOf(content) != -1)
                    vowelCount++;
                else
                    novowelCount++;
            }
        }
        if (simbCount != 0) strCount++;
        Console.WriteLine("Всего символов: {0}", simbCount);
        Console.WriteLine("Гласных символов: {0}", vowelCount);
        Console.WriteLine("Согласных символов: {0}", novowelCount);
        Console.WriteLine("Всего строк: {0}", strCount);
    }
}
