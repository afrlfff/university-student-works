namespace Utils
{
    using System;

    public class Utils
    {
        public static bool IsItFormattable(object x)
        {
            return x is System.IFormattable;
        }
        public static int Greater(int a, int b)
        {
            if (a > b)
                return a;
            else
                return b;
        }
        public static void Swap(ref int a, ref int b)
        {
            int temp;
            temp = a;
            a = b;
            b = temp;
        }
        public static bool Factorial(int n, out int answer)
        {
            int k;        // loop counter
            int f;        // working value
            bool ok = true; // true if ok, false if not

            // Check the input value

            if (n < 0)
                ok = false;

            try
            {
                checked
                {
                    f = 1;
                    for (k = 2; k <= n; ++k)
                    {
                        f = f * k;
                    }

                    // Here is a terse alternative
                    // for (f=1,k=2;k<=n;++k)
                    //     f*=k;

                }
            }
            catch (Exception)
            {
                f = 0;
                ok = false;
            }

            // assign result value                
            answer = f;

            // return to caller
            return ok;
        }
        public static bool RecursiveFactorial(int n, out int f)
        {
            bool ok = true;

            // Trap negative inputs
            if (n < 0)
            {
                f = 0;
                ok = false;
            }

            if (n <= 1)
                f = 1;
            else
            {
                try
                {
                    int pf;
                    checked
                    {
                        ok = RecursiveFactorial(n - 1, out pf);
                        f = n * pf;
                    }
                }
                catch (Exception)
                {
                    f = 0;
                    ok = false;
                }

            }

            return ok;
        }
    }
}