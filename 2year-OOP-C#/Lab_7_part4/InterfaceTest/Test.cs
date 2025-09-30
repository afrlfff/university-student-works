namespace Utils
{
    public class Test
    {
        public static void Main()
        {
            int i = 0;
            ulong ul = 0;
            string s = "Test";
            if (Utils.IsItFormattable(i))
                Console.WriteLine("i is Formattable");
            else
                Console.WriteLine("i is not Formattable");
            if (Utils.IsItFormattable(ul))
                Console.WriteLine("ul is Formattable");
            else
                Console.WriteLine("ul is not Formattable");
            if (Utils.IsItFormattable(s))
                Console.WriteLine("s is Formattable");
            else
                Console.WriteLine("s is not Formattable");
        }
    }
}