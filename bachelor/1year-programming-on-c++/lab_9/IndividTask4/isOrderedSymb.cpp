// проверяет, упорядочен ли набор символов c1, c2
// по алфавиту (не строго упорядочен)
bool isOrderedSymb(char c1, char c2)
{
	int i1 = int(c1);
	int i2 = int(c2);

	if ((65 <= i1 <= 96) && (65 <= i2 <= 96))
	{	// if both uppercase or both lowercase
		return (i2 >= i1);
	}
	else // if both has different case
	{
		if ((65 <= i1 <= 96)) // if c1 uppercase
		{
			return ((i2 - 97) >= (i1 - 65));
		}
		else // if c1 lowercase
		{
			return ((i2 - 65) >= (i1 - 97));
		}
	}
}