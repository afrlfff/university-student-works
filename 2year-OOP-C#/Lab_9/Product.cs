namespace Stores
{
    public enum FoodType
    {
        Fruit, Vegetable, Meat, Fish, Pan, Drink, Frozen, Grain, Canned, Confectionary
    };
    public interface IQRcode
    {
        public void Display();
    }
    public interface IProduct
    {
        public void Display();
        public TimeSpan TimeToExpire();
    };
    public class Product: IProduct
    {
        public class QRcode
        {
            // the code will stored as a matrix of black/white pixels
            // or in other words as a matrix of 1/0
            public int[] Code { get; private set; }
            private static List<int[]> usingCodes = new List<int[]>();

            public QRcode()
            {
                Code = GenerateNew();
                usingCodes.Add(Code);
            }
            public QRcode(int[] code)
            {
                Code = code;
                usingCodes.Add(Code);
            }
            public void Display()
            {
                Console.WriteLine("QRcode representation: ");
                for (int i = 0; i < Code.Length; i++)
                {
                    Console.WriteLine(Code[i]);
                }
            }
            private static int[] GenerateNew()
            {
                int[] code = new int[20 * 20];
                int codeKey = 0;

                // set a standard value to code
                for (int i = 0; i < code.Length; i++)
                {
                    code[i] = 0;
                }

                // increasing value of code representation while it is not unique
                while (usingCodes.Contains(code))
                {
                    codeKey++;
                    string binary = Convert.ToString(codeKey, 2);

                    // restore the code
                    for (int i = 0; i < code.Length; i++)
                    {
                        code[i] = 0;
                    }

                    // add binary code to the end
                    for (int i = code.Length - 1, j = 0; j < binary.Length; i--, j++)
                    {
                        code[i] = (int)(binary[binary.Length - (j + 1)] - '0');
                    }
                }
                return code;
            }
        }
        public string Name { get; private set; }
        public string Description { get; private set; }
        public FoodType Type { get; private set; }
        public decimal Price { get; private set; }
        public DateTime ExpiryDate { get; private set; }
        public QRcode QrCode { get; private set; }
        
        public Product(string name, string description, decimal price, QRcode qr, FoodType type, DateTime expiryDate)
        {
            QrCode = qr;
            Type = type;
            ExpiryDate = expiryDate;
            Name = name;
            Description = description;
            Price = price;
        }
        public void Display()
        {
            Console.WriteLine($"Name: {Name}");
            Console.WriteLine($"Description: {Description}");
            Console.WriteLine($"Type: {Type}");
            Console.WriteLine($"Price: {Price}");
            Console.WriteLine($"Expiry Date: {ExpiryDate}");
        }
        public TimeSpan TimeToExpire()
        {
            return ExpiryDate - DateTime.Now;
        }
    };
}