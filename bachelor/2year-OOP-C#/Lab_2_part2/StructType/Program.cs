using System;

enum AccountType { Cheching, Deposit}

class StructType
{
    public struct BankAccount
    {
        public long accNo;
        public decimal accBal;
        public AccountType accType;
    }
    public static void Main(string[] args)
    {
        BankAccount goldAccount;
        goldAccount.accNo = 1200301;
        goldAccount.accBal = 500000;
        goldAccount.accType = AccountType.Cheching;
        Console.WriteLine("Номер аккаунта: {0}", goldAccount.accNo);
        Console.WriteLine("Баланс аккаунта: {0}", goldAccount.accBal);
        Console.WriteLine("Тип аккаунта: {0}", goldAccount.accType);
    }
}