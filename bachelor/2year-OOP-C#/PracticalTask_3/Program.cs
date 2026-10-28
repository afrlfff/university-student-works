using System;
using SingletonExample;
using MyApp;

namespace Program
{
    class Program
    {
        static void Main(string[] args)
        {
            /*
                FirstClass first = new FirstClass();
                SecondClass second = new SecondClass();
                Console.WriteLine("Singleton name in first class: " + first.getName());
                Console.WriteLine("Singleton name in second class: " + second.getName());
                Console.Read();
            */
            NoSingleton ns1 = new NoSingleton();
            NoSingleton ns2 = new NoSingleton();
            NoSingleton ns3 = new NoSingleton();
            UseSingleton us1 = UseSingleton.Instance;
            UseSingleton us2 = UseSingleton.Instance;
            UseSingleton us3 = UseSingleton.Instance;
        }
    }
}
