using System;
using /*MyApp*/WaveForecast;

namespace Program
{
    public class Program
    {
        static void Main(string[] args)
        {
            /*
                Subject subject = new Subject();
                Observer observer = new Observer(subject, "Center", "\t\t");
                Observer observer2 = new Observer(subject, "Right", "\t\t\t\t");
                subject.Go();
                Console.Read();
            */
            Subject subject = new Subject();
            Observer observer1 = new Observer(subject, "Saint Petersburg");
            Observer observer2 = new Observer(subject, "Moscow");
            Observer observer3 = new Observer(subject, "Pushkin");
            subject.Go();
            Console.Read();
        }
    }
}