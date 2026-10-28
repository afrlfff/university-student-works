using Stores;

namespace Program
{
    public class Test
    {
        public static void Main(string[] args)
        {
            GroceryStore myStore = new GroceryStore(
                "My Store", "123 Main St",new TimeSpan(10, 0, 0), new TimeSpan(22, 0, 0));
            myStore.Display();

            // Initialize products
            Product milk = new Product("Milk", "", 85, new QRcode(), FoodType.Drink, new DateTime(2024, 1, 5));
            Product Apples = new Product("Apples", "1 kg", 400, new QRcode(), FoodType.Fruit, new DateTime(2024, 1, 30));
            Product ToastedPan = new Product("Toasted Pan", "", 99, new QRcode(), FoodType.Pan, new DateTime(2024, 1, 5));
            myStore.AddProduct(milk, 30);
            myStore.AddProduct(Apples, 10);
            myStore.AddProduct(ToastedPan, 10);

            // Display inventory
            Console.WriteLine("Current Store inventory:");
            myStore.PrintProducts();

            // Remove some products and display inventory
            myStore.RemoveProduct(milk, 10);
            Console.WriteLine("New Store inventory:");
            myStore.PrintProducts();
        }
    }
}