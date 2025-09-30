using SingletonExample;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace MyApp
{
    class UseSingleton
    {
        protected static int number = 0;

        /// Защищенный конструктор нужен, чтобы предотвратить
        // создание экземпляра класса Singleton
        protected UseSingleton()
        {
            number += 1;
            Console.WriteLine("New Singleton object was created.\n\tnumber =  " + number);
        }

        private sealed class SingletonCreator
        {
            private static readonly UseSingleton instance = new UseSingleton();
            public static UseSingleton Instance { get { return instance; } }
        }
        public string getNumber
        {
            get
            {
                return number.ToString();
            }
        }
        public static UseSingleton Instance
        {
            get { return SingletonCreator.Instance; }
        }
    }
    class NoSingleton
    {
        private static int number = 0;

        public NoSingleton()
        {
            number++;
            Console.WriteLine("New NoSingleton object was created.\n\tnumber =  " + number);
        }
    }
}
