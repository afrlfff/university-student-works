using System;

using Birds;

namespace Program
{
    class Program
    {
        static void Main(string[] args)
        {
            Duck mallard = new MallardDuck();
            mallard.performQuack();
            mallard.performFly();
            Duck wood = new WoodDuck();
            wood.performQuack();
            wood.performFly();
            System.Console.ReadKey();
        }
    }
}