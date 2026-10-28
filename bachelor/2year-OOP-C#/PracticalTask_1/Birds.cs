



namespace Birds
{
    // ========== BASE ========== //

// Duck base
    class Duck
    {
        protected FlyBehavior flybehavior;
        protected QuackBehavior quackbehavior;
        protected SwimBehavior swimbehavior;

        public Duck() { }
        public void performFly()
        {
            flybehavior.fly();
        }
        public void performQuack()
        {
            quackbehavior.quack();
        }
        public void performSwim()
        {
            swimbehavior.swim();
        }
    }
// Fly base
    interface FlyBehavior
    {
        void fly();
    }
// Quack base
    interface QuackBehavior
    {
        void quack();
    }
// Swim base
    interface SwimBehavior
    {
        void swim();
    }

    // ========== INHERITORS ========== //

// Duck Inheritors
    class MallardDuck : Duck
    {
        public MallardDuck()
        {
            quackbehavior = new Quack();
            flybehavior = new FlyWithWings();
            swimbehavior = new CanSwim();
            System.Console.WriteLine("I MallardDuck");
        }
    }
    class WoodDuck : Duck
    {
        public WoodDuck()
        {
            quackbehavior = new Silence();
            flybehavior = new FlyNoWay();
            swimbehavior = new CanNotSwim();
            System.Console.WriteLine("I WoodDuck");
        }
    }

// Fly inheritors
    class FlyWithWings : FlyBehavior
    {
        public void fly()
        {
            System.Console.WriteLine("I can fly");
        }
    }
    class FlyNoWay : FlyBehavior
    {
        public void fly()
        {
            System.Console.WriteLine("I can`t fly");
        }
    }

// Quack Inheritors
    class Quack : QuackBehavior
    {
        public void quack()
        {
            System.Console.WriteLine("Quack");
        }
    }
    class Silence : QuackBehavior
    {
        public void quack()
        {
            System.Console.WriteLine("Silence");
        }
    }
// Swim Inheritors
    class CanSwim : SwimBehavior
    {
        public void swim()
        {
            System.Console.WriteLine("I can swim");
        }
    }
    class CanNotSwim : SwimBehavior
    {
        public void swim()
        {
            System.Console.WriteLine("I can not swim");
        }
    }
}