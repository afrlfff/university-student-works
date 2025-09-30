namespace FileDetails
{
    class CreateAccount
    {
        static void Main()
        {
            BankAccount berts = NewBankAccount();
            Write(berts);

            TestDeposit(berts);
            Console.WriteLine("NEW: berts after making deposit: ");
            Write(berts);
            
            Console.Write("Enter amount to withdraw: ");
            try
            {
                if (berts.WithDraw(decimal.Parse(Console.ReadLine())))
                    Console.WriteLine("Withdraw was succesful.");
                else
                    Console.WriteLine("Withdraw was not made.");
            }
            catch (Exception)
            {
                Console.WriteLine("Incorrect amount was entered");
                return;
            }
            
            Console.WriteLine("NEW: berts after withdraw: ");
            Write(berts);



            BankAccount freds = NewBankAccount();
            Write(freds);

            TestDeposit(freds);
            Console.WriteLine("NEW: freds after making deposit: ");
            Write(freds);
            
            Console.Write("Enter amount to withdraw: ");
            try
            {
                if (berts.WithDraw(decimal.Parse(Console.ReadLine())))
                    Console.WriteLine("Withdraw was succesful.");
                else
                    Console.WriteLine("Withdraw was not made.");
            }
            catch (Exception)
            {
                Console.WriteLine("Incorrect amount was entered.");
                return;
            }
            
            Console.WriteLine("NEW: freds after withdraw: ");
            Write(freds);
        }

        public static void TestDeposit(BankAccount acc)
        {
            Console.Write("Enter amount to deposit: ");
            decimal amount = decimal.Parse(Console.ReadLine());
            acc.Deposit(amount);
        }
        static BankAccount NewBankAccount()
        {
            BankAccount created = new BankAccount();

            // Console.Write("Enter the account number   : ");
            // long number = long.Parse(Console.ReadLine());

            Console.Write("Enter the account balance : ");
            try
            {
                decimal balance = decimal.Parse(Console.ReadLine());
                created.Populate(balance);
            }
            catch (Exception)
            {
                Console.WriteLine("Incorrect balance was entered.");
                Environment.Exit(1);
            }

            // created.accNo = number;
            // created.accBal = balance;
            // created.accType = AccountType.Checking;

            return created;
        }

        static void Write(BankAccount toWrite)
        {
            Console.WriteLine("Account number is {0}", toWrite.Number());
            Console.WriteLine("Account balance is {0}", toWrite.Balance());
            Console.WriteLine("Account type is {0}", toWrite.Type());
            Console.WriteLine();
        }
    }
}