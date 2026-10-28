namespace FileDetails
{
    internal class BankAccount
    {
        private long accNo;
        private decimal accBal;
        private AccountType accType;
        private static long nextAccNo = 123;

        public bool WithDraw(decimal amount)
        {
            if (amount <= accBal)
            {
                accBal -= amount;
                return true;
            }
            else
            {
                return false;
            }
        }
        public decimal Deposit(decimal amount)
        {
            accBal += amount;
            return accBal;
        }
        private static long NextNumber()
        {
            return nextAccNo++;
        }
        public void Populate(decimal balance)
        {
            accNo = NextNumber();
            accBal = balance;
            accType = AccountType.Checking;
        }
        public long Number() { return accNo; }
        public decimal Balance() { return accBal; }
        public AccountType Type() { return accType; }
    }
}
