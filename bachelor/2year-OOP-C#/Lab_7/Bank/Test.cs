namespace Bank
{
    public class Test
    {
        public static void Main()
        {
            BankAccount account = new BankAccount();
            BankAccount b1 = new BankAccount();
            BankAccount b2 = new BankAccount();
            b1.Populate(100);
            b2.Populate(100);

            Console.WriteLine("Type of b1 Account: {0}", b1.Type());
            Console.WriteLine("Number of b1 Account: {0}", b1.Number());
            Console.WriteLine("Balance of b1 Account: {0}$", b1.Balance());
            Console.WriteLine("Type of b2 Account: {0}", b2.Type());
            Console.WriteLine("Number of b2 Account: {0}", b2.Number());
            Console.WriteLine("Balnce of b2 Account: {0}$", b2.Balance());
            b1.TransferForm(ref b2, 10);
            Console.WriteLine("Type of b1 Account: {0}", b1.Type());
            Console.WriteLine("Number of b1 Account: {0}", b1.Number());
            Console.WriteLine("Balance of b1 Account: {0}$", b1.Balance());
            Console.WriteLine("Type of b2 Account: {0}", b2.Type());
            Console.WriteLine("Number of b2 Account: {0}", b2.Number());
            Console.WriteLine("Balnce of b2 Account: {0}$", b2.Balance());
        }
    }
}