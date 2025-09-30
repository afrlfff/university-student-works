using System;

enum AccountType { Checking, Deposit};
class BankApplication
{
    public static void Main(string[] args)
    {
        AccountType goldAccount = AccountType.Checking;
        AccountType platinumAccount = AccountType.Deposit;
        Console.WriteLine("Тип золотого аккаунта: {0}", goldAccount);
        Console.WriteLine("Тип платинового аккаунта {0}", platinumAccount);
    }
}