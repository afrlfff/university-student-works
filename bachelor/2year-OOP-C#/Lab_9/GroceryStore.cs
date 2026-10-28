namespace Stores
{
    public abstract class Store
    {
        public string Name { get; set; }
        public string Location { get; set; }
        public decimal Balance { get; set; }
        public TimeSpan OpeningTime { get; set; } // Represents 10:00 AM
        public TimeSpan ClosingTime { get; set; } // Represents 10:00 PM

        public Store(string name, string location, TimeSpan openingTime, TimeSpan closingTime)
        {
            Name = name;
            Location = location;
            Balance = 0;
            OpeningTime = openingTime;
            ClosingTime = closingTime;
        }
        public void Display()
        {
            Console.WriteLine($"Name: {Name}");
            Console.WriteLine($"Location: {Location}");
            Console.WriteLine($"Balance: {Balance}");
            Console.WriteLine($"Opening time: {OpeningTime}");
            Console.WriteLine($"Closing time: {ClosingTime}");
        }
        public abstract void AddProduct(Product product, int quantity);
        public abstract void RemoveProduct(Product product, int quantity);
        public abstract void SellProduct(Product product, int quantity);
        public abstract void PrintProducts();
        public abstract List<Product> RemoveExpiredProducts();
    }
    public abstract class Warehouse
    {
        public string Name { get; set; }
        public string Location { get; set; }

        public Warehouse(string name, string location)
        {
            Name = name;
            Location = location;
        }
        public void Display()
        {
            Console.WriteLine($"Name: {Name}");
            Console.WriteLine($"Location: {Location}");
        }
        public abstract void AddProduct(Product product, int quantity);
        public abstract void RemoveProduct(Product product, int quantity);
        public abstract void PrintProducts();
        public abstract void PrintExpiredProducts();
        public abstract List<Product> RemoveExpiredProducts();
    }

    public class GroceryStore : Store
    {
        public class FoodWarehouse : Warehouse
        {
            private readonly Dictionary<Product, int> products;

            public FoodWarehouse(string name, string location): base(name, location)
            {
                products = new Dictionary<Product, int>();
            }
            public override void AddProduct(Product product, int quantity)
            {
                foreach (var p in products)
                {
                    if (p.Key.QrCode == product.QrCode)
                    {
                        products[p.Key] += quantity;
                        return;
                    }
                }
                products.Add(product, quantity);
            }
            public override void RemoveProduct(Product product, int quantity)
            {
                foreach (var p in products)
                {
                    if (p.Key.QrCode == product.QrCode)
                    {
                        if (quantity < p.Value)
                        {
                            products[p.Key] -= quantity;
                        }
                        else
                        {
                            products.Remove(product);
                        }
                        return;
                    }
                }
                products.Remove(product);
            }
            public override void PrintProducts()
            {
                Console.WriteLine("Products:");
                foreach (var product in products)
                {
                    product.Key.Display();
                    System.Console.WriteLine($"Total quantity: {product.Value}\n");
                }
            }
            public override void PrintExpiredProducts()
            {
                Console.WriteLine("Expired Products:");
                foreach (var product in products)
                {
                    if (product.Key.TimeToExpire().TotalSeconds <= 0)
                    {
                        product.Key.Display();
                    }
                }
            }
            public override List<Product> RemoveExpiredProducts()
            {
                List<Product> expiredProducts = new List<Product>();
                foreach (var product in products)
                {
                    if (product.Key.TimeToExpire().TotalSeconds <= 0)
                    {
                        expiredProducts.Add(product.Key);
                        products.Remove(product.Key);
                    }
                }
                return expiredProducts;
            }
        };


        private FoodWarehouse warehouse;

        public GroceryStore(string name, string location, TimeSpan openingTime, TimeSpan closingTime) : base(name, location, openingTime, closingTime)
        {
            warehouse = new FoodWarehouse(Name + "_Warehouse", Location);
        }
        public override void AddProduct(Product product, int quantity)
        {
            warehouse.AddProduct(product, quantity);
        }
        public override void RemoveProduct(Product product, int quantity)
        {
            warehouse.RemoveProduct(product, quantity);
        }
        public override void SellProduct(Product product, int quantity)
        {
            Balance += product.Price;
            warehouse.RemoveProduct(product, quantity);
        }
        public override void PrintProducts()
        {
            warehouse.PrintProducts();
        }
        public override List<Product> RemoveExpiredProducts()
        {
            return warehouse.RemoveExpiredProducts();
        }
    }
}