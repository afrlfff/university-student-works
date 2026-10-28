using System.Collections;

namespace WaveForecast
{
    class Simulator : IEnumerable
    {
        public int countOfValues = 5;
        private int[] temperatures = { 25, 20, 28, 23, 27 };
        private int[] humidities = { 50, 55, 60, 45, 52 };
        private int[] pressures = { 1010, 1005, 1008, 1003, 1007 };

        public IEnumerator GetEnumerator()
        {
            for (int i = 0; i < countOfValues; i++)
                yield return new int[] { temperatures[i], humidities[i], pressures[i] };
        }
    }
    interface IObserver
    {
        void Update(int temperature, int humidity, int pressure);
    }
    class Observer : IObserver
    {
        Subject subject;
        string name;
        int temperature;
        int humidity;
        int pressure;

        public Observer(Subject subject, string name)
        {
            this.subject = subject;
            this.name = name;
            this.temperature = 0;
            this.humidity = 0;
            this.pressure = 0;
            subject.Notify += Update;
        }

        public void Update(int subjectTemperature, int subjectHumidity, int subjectPressure)
        {
            temperature = subjectTemperature;
            humidity = subjectHumidity;
            pressure = subjectPressure;
            Console.WriteLine(name + ":" + 
                              "\n\tTemperature: " + temperature + 
                              "\n\tHumidity: " + humidity + 
                              "\n\tPressure: " + pressure);
        }
    }

    class Subject
    {
        public delegate void Callback(int temperature, int humidity, int pressure);

        public event Callback Notify;

        Simulator simulator = new Simulator();

        const int speed = 200;

        //public int[] SubjectState { get; set; }
        public int[] SubjectState = new int[3];

        public void Go()
        {
            new Thread(new ThreadStart(Run)).Start();
        }

        void Run()
        {
            int k = 1;
            foreach (var s in simulator)
            {
                Console.WriteLine("Day " + k);
                SubjectState = (int[])s;
                Notify(SubjectState[0], SubjectState[1], SubjectState[2]);
                Thread.Sleep(speed); // milliseconds
                k++;
            }
        }
    }
}
