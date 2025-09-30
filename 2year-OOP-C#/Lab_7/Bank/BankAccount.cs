namespace Bank
{
    class BankAccount
    {
        private long accNo;
        private decimal accBal;
        private AccountType accType;
        private static long nextNumber = 123;

        public void TransferForm(ref BankAccount accForm, decimal amount)
        {
            if (Withdraw(amount))
            {
                accForm.Deposit(amount);
                Console.WriteLine("\nTranfer was succesful.");
            }
            else
            {
                Console.WriteLine("\nTranfer was not made.");
            }
        }
        public void Populate(decimal balance)
        {
            accNo = NextNumber();
            accBal = balance;
            accType = AccountType.Checking;
        }

        public bool Withdraw(decimal amount)
        {
            bool sufficientFunds = accBal >= amount;
            if (sufficientFunds)
            {
                accBal -= amount;
            }
            return sufficientFunds;
        }

        public decimal Deposit(decimal amount)
        {
            accBal += amount;
            return accBal;
        }
        public long Number()
        {
            return accNo;
        }

        public decimal Balance()
        {
            return accBal;
        }

        public string Type()
        {
            return Enum.Format(typeof(AccountType), accType, "G");
        }

        private static long NextNumber()
        {
            return nextNumber++;
        }
    }
}