namespace Games
{
    public class FoolGame
    {
        // Масть
        public enum CardSuit { Spades, Clubs, Hearts, Diamonds }

        // Карта
        public class Card
        {
            public int Power { get; private set; }
            public CardSuit Suit { get; private set; }

            public Card(CardSuit suit, int power)
            {
                Power = power;
                Suit = suit;
            }
            public Card(int suit, int power)
            {
                Power = power;
                if (suit == 0) Suit = CardSuit.Spades;
                if (suit == 1) Suit = CardSuit.Clubs;
                if (suit == 2) Suit = CardSuit.Hearts;
                if (suit == 3) Suit = CardSuit.Diamonds;
            }
        }

        private static List<Card> packCards = new List<Card>(36); // карты в колоде
        private static List<Card> cardsOnTable = new List<Card>(); // карты на столе
        private static CardSuit royalSuit; // козырная масть
        private static StreamWriter protocolFile;

        // Функция для записи в файл
        private static void LogToFile(string message)
        {
            Console.Write(message);
            protocolFile.Write(message);
        }

        // Запуск игры
        public static void StartGame()
        {
            string filePath = "protocol_" + DateTime.Now.ToString("dd_MM_yyyy_HH_mm_ss") + ".txt";
            protocolFile = File.CreateText(filePath);

            Computer computer = new Computer("YourPC");
            Human player = new Human("You");
            
            // Инициализация карт
            for (int i = 0; i < 36; i++)
            {
                packCards.Add(new Card(i / 9, 6 + i % 9));
            }

            // Раздаем карты игроку
            Random random = new Random();
            while (player.playerCards.Count() < 6)
            {
                Card randomCard = packCards[random.Next(0, packCards.Count)];
                player.playerCards.Add(randomCard);
                packCards.Remove(randomCard);
            }

            // Раздаем карты компьютеру
            while (computer.playerCards.Count < 6)
            {
                Card randomCard = packCards[random.Next(0, packCards.Count)];
                computer.playerCards.Add(randomCard);
                packCards.Remove(randomCard);
            }

            // Установка козырной масти
            int randomValue = random.Next(0, 3 + 1);
            if (randomValue == 0) royalSuit = CardSuit.Spades;
            if (randomValue == 1) royalSuit = CardSuit.Clubs;
            if (randomValue == 2) royalSuit = CardSuit.Hearts;
            if (randomValue == 3) royalSuit = CardSuit.Diamonds;

            // Опрделяем, кто первый ходит
            if (player.MinRoyalCard() > computer.MinRoyalCard()) { computer.PlayerOrder = 0; player.PlayerOrder = 1; }
            else { computer.PlayerOrder = 1; player.PlayerOrder = 0; }
            LogToFile("Козырная масть: " + royalSuit.ToString() + '\n');

            // Сама игра
            while (true)
            {
                // Если первый ходит компьютер
                if (computer.PlayerOrder == 0)
                {
                    // Реализуем атаку со строны компьютера
                    // и защиту со стороны игрока
                    LogToFile("Атакует " + computer.Name + '!' +'\n');
                    Attack(computer, player);
                    ShowCardsOnTable();
                    Defence(computer, player);
                    LogToFile("Ваши карты: " + '\n');
                    player.DisplayCards();
                    LogToFile("\n");

                    // Добираем карты из колоды после атаки и защиты
                    while (true)
                    {
                        // добавляем карты компьютеру
                        if (packCards.Count() > 0 && computer.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            computer.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        // игроку
                        if (packCards.Count() > 0 && player.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            player.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        if (packCards.Count() == 0) break;
                        if (computer.playerCards.Count() >= 6 && player.playerCards.Count() >= 6) break;//<--------------------------
                    }

                    // Определяем, завершена ли игра
                    if (computer.playerCards.Count() == 0) { LogToFile(computer.Name + " выиграл!" + '\n'); return; }
                    if (player.playerCards.Count() == 0) { LogToFile(player.Name + " выиграл!" + '\n'); return; }

                    // Реализуем атаку со стороны игрока
                    // и зашиту со стороны компьютера
                    LogToFile("Атакует " + player.Name + '!');
                    LogToFile("Если вы атакуете несколькими картами, то выбирайте только карты одного ранга!" + '\n');
                    Attack(player, computer);
                    ShowCardsOnTable();
                    Defence(player, computer);
                    LogToFile("Ваши карты: " + '\n');
                    player.DisplayCards();
                    LogToFile("\n");

                    // Добираем карты из колоды после атаки и защиты
                    while (true)
                    {
                        // добавляем карты игроку
                        if (packCards.Count() > 0 && player.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            player.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        // компьютеру
                        if (packCards.Count() > 0 && computer.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            computer.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        if (packCards.Count() == 0) break;
                        if (computer.playerCards.Count() >= 6 && player.playerCards.Count() >= 6) break;//<--------------------------
                    }
                    if (player.playerCards.Count() == 0) { LogToFile(player.Name + " выиграл!" + '\n'); return; }
                    if (computer.playerCards.Count() == 0) { LogToFile(computer.Name + " выиграл!" + '\n'); return; }
                }

                // если первым ходит игрок
                if (player.PlayerOrder == 0)
                {
                    // Реализуем атаку со стороны кигрока
                    LogToFile("Атакует " + player.Name + '!' + '\n');
                    LogToFile("Если вы атакуете несколькими картами, то выбирайте только карты одного ранга!" + '\n');
                    Attack(player, computer);
                    ShowCardsOnTable();
                    Defence(player, computer);
                    LogToFile("Ваши карты: " + '\n');
                    player.DisplayCards();
                    LogToFile("\n");

                    // Выдача карт после атаки и защиты
                    while (true)
                    {
                        // добавляем карты игроку
                        if (packCards.Count() > 0 && player.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            player.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        // компьютеру
                        if (packCards.Count() > 0 && computer.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            computer.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        if (packCards.Count() == 0) break;
                        if (computer.playerCards.Count() >= 6 && player.playerCards.Count() >= 6) break;//<--------------------------
                    }

                    // Определяем, завершена ли игра, и выводим имя победителя
                    if (player.playerCards.Count() == 0) { LogToFile(player.Name + " выиграл!" + '\n'); return; }
                    if (computer.playerCards.Count() == 0) { LogToFile(computer.Name + " выиграл!" + '\n'); return; }

                    // Реализация атаки со стороны компьютера, защиту со стороны игрока
                    LogToFile("Атакует " + computer.Name + '!' + '\n');
                    Attack(computer, player);
                    ShowCardsOnTable();
                    Defence(computer, player);
                    LogToFile("Ваши карты: " + '\n');
                    player.DisplayCards();
                    LogToFile("\n");

                    // Выдача карт после атаки и защиты
                    while (true)
                    {
                        // Добавляем карты компьютеру
                        if (packCards.Count() > 0 && computer.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            computer.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        // Игроку
                        if (packCards.Count() > 0 && player.playerCards.Count() < 6)
                        {
                            Card randomCard = packCards[random.Next(0, packCards.Count)];
                            player.playerCards.Add(randomCard);
                            packCards.Remove(randomCard);
                        }
                        if (packCards.Count() == 0) break;
                        if (computer.playerCards.Count() >= 6 && player.playerCards.Count() >= 6) break;//<--------------------------
                    }

                    // Определяем, завершена ли игра, и выводим победителя
                    if (computer.playerCards.Count() == 0) { LogToFile(computer.Name + " выиграл!" + '\n'); return; }
                    if (player.playerCards.Count() == 0) { LogToFile(player.Name + " выиграл!" + '\n'); return; }
                }
            }

        }

        // Вывод карт, которые необходимо отбить
        private static void ShowCardsOnTable()
        {
            LogToFile("Карты на столе: " + '\n');
            int i = 0;
            foreach (Card card in cardsOnTable)
            {
                i++;
                LogToFile(i + ". Suit: " + card.Suit + "; Power: " + card.Power + '\n');
            }
        }

        // Атака, ход делает первый аргумент ф-ии, защищаться будет второй
        private static void Attack(Player attacker, Player defender)
        {
            // Если атакер - человек
            if (attacker is Human)
            {
                LogToFile("Выберете карты для атаки:" + '\n');
                int i = 0;
                LogToFile("0. Завершить ход." + '\n');

                // Выбираем одну или несколько карт (пользователь должен соблюдать правило при выборе нескольких карт - 
                // Они могут быть только одного ранга
                LogToFile("У противника " + defender.playerCards.Count() + " карт" + '\n');
                while (attacker.playerCards.Count > 0 && cardsOnTable.Count != defender.playerCards.Count())
                {
                    attacker.DisplayCards();
                    LogToFile("\n");
                    int crd = int.Parse(Console.ReadLine()); // номер карты, которую выбрал игрок

                    // если игрок завершает ход
                    if (crd == 0)
                    {
                        if (i > 0) break;
                        else LogToFile("Выберете хотя бы одну карту" + '\n');
                    }
                    i++;
                    
                    // Добавляем карты на стол и убираем их у игрока
                    if (crd > 0) cardsOnTable.Add(attacker.playerCards[crd - 1]);
                    if (crd > 0) attacker.playerCards.RemoveAt(crd - 1);
                }
            }
            // если атаакует компьютер
            if (attacker is Computer)
            {
                Random random = new Random();
                int p = random.Next(0, 2); // выбирает случайное значение для хода
                switch (p)
                {
                    //компьютер выбрал ход одной картой
                    case 0:
                        //выбираем самую младшую карту, чтобы от неё отбиться
                        attacker.playerCards = attacker.playerCards.OrderBy(c => c.Power).ToList();
                        cardsOnTable.Add(attacker.playerCards[0]);
                        attacker.playerCards.RemoveAt(0);
                        break;
                    //компьютер выбрал ход несколькими картами одного ранга, если это возможно
                    case 1:
                        //выбираем самые младшие парные карты 
                        int min = 15;
                        for (int i = 6; i <= 14; i++)               //<--------------------------
                        {
                            if (attacker.playerCards.Where(c => c.Power == i).Count() > 1 && min > i) min = i;
                        }
                        if (min == 15) goto case 0; //парных карт нет
                        //у защищаегося должно хватать карт для обороны
                        int num = attacker.playerCards.Where(c => c.Power == min).Count();
                        for (int i = 0; i < num && i < defender.playerCards.Count; i++)
                        {
                            cardsOnTable.Add(attacker.playerCards.Where(c => c.Power == min).ToList()[0]);
                            attacker.playerCards.Remove(attacker.playerCards.Where(c => c.Power == min).ToList()[0]);
                        }
                        break;
                }
            }
        }

        // Защита, первый аргумент атакует, второй - защищается
        private static void Defence(Player attacker, Player defender)
        {
            // если защищается человек
            if (defender is Human)
            {
                LogToFile("Вы можете забрать карты (нажмите 1), либо отбить их (0)." + '\n');
                defender.DisplayCards();
                LogToFile("\n");
                int num = int.Parse(Console.ReadLine()); // номер карты, которую выбрал игрок

                // если игрок забирает карты
                if (num == 1)
                {
                    defender.playerCards.AddRange(cardsOnTable);
                    cardsOnTable = new List<Card>();
                    return;
                }

                // карты игрока, которыми он бил карты на столе. если игрок не сможет побить карты на столе, то они отходят к игроку
                List<Card> cards_to_delete = new List<Card>();

                // проходим по каждой карте на столе и бьём её
                foreach (Card card in cardsOnTable)
                {
                    defender.DisplayCards();
                    LogToFile("\n");
                    LogToFile("Выберете карту сильнее, чем " + card.Suit + " " + card.Power + ". Если вы не можете побить её нажмите 0" + '\n');
                    num = int.Parse(Console.ReadLine());
                    if (num == 0) break;
                    if (defender.playerCards[num - 1].Power > card.Power && card.Suit != royalSuit && defender.playerCards[num - 1].Suit == card.Suit)
                    { cards_to_delete.Add(defender.playerCards[num - 1]); LogToFile("Карта бита" + '\n'); defender.playerCards.RemoveAt(num - 1); }//карта на столе не козырная, бьём не козырной
                    else if (defender.playerCards[num - 1].Power > card.Power && card.Suit == royalSuit && defender.playerCards[num - 1].Suit == royalSuit)
                    { cards_to_delete.Add(defender.playerCards[num - 1]); LogToFile("Карта бита" + '\n'); defender.playerCards.RemoveAt(num - 1); }//карта на столе козырная, бьём козырной
                    else if (defender.playerCards[num - 1].Suit == royalSuit && card.Suit != royalSuit)
                    { cards_to_delete.Add(defender.playerCards[num - 1]); LogToFile("Карта бита" + '\n'); defender.playerCards.RemoveAt(num - 1); }//карта на столе не козырная, бьём козырной
                    else
                    {
                        LogToFile("Карта не бита" + '\n');
                    }
                }

                Random random = new Random();
                num = random.Next(0, 3); // с шансом 2 к 3 компьютер подкидывает карты
                List<Card> thrown_cards = new List<Card>(); // подкинутые карты
                if (num != 0 && attacker.playerCards
                    .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power).Contains(c.Power)).Count() > 0)
                // подбрасывать можно все карты того же ранга, которые участвуют в данном заходе: как те, которыми атакуют, так и те, которыми отбиваются;
                {
                    // случайное количество карт для подкидывания (минимум 1)
                    num = random.Next(1, attacker.playerCards
                        .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power).Contains(c.Power)).Count() + 1);

                    //подкидывать можно максимум 5 карт
                    if (num > 5) num = 5;
                    
                    // подкидываем карту
                    for (int i = 0; i < num && i < defender.playerCards.Count(); i++)
                    {
                        thrown_cards.Add(attacker.playerCards
                            .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power).Contains(c.Power)).ToList()[i]);
                    }
                }

                // если есть подкинутые краты
                if (thrown_cards.Count > 0)
                {
                    LogToFile("Подкинуты карты:" + '\n');
                    int i = 0;
                    thrown_cards.ForEach(c => { i++; LogToFile(i + ". " + c.Suit + ' ' + c.Power + '\n'); });

                    // бьем все подкинутые карты
                    foreach (Card card in thrown_cards)
                    {
                        defender.DisplayCards();
                        LogToFile("\n");
                        LogToFile("Выберете карту сильнее, чем " + card.Suit + " " + card.Power + ". Если вы не можете побить её нажмите 0" + '\n');
                        num = int.Parse(Console.ReadLine());
                        if (num == 0) break;
                        if (defender.playerCards[num - 1].Power > card.Power && card.Suit != royalSuit && defender.playerCards[num - 1].Suit == card.Suit)
                        { cards_to_delete.Add(card); LogToFile("Карта бита" + '\n'); defender.playerCards.RemoveAt(num - 1); }//карта на столе не козырная, бьём не козырной
                        else if (defender.playerCards[num - 1].Power > card.Power && card.Suit == royalSuit && defender.playerCards[num - 1].Suit == royalSuit)
                        { cards_to_delete.Add(card); LogToFile("Карта бита" + '\n'); defender.playerCards.RemoveAt(num - 1); }//карта на столе козырная, бьём козырной
                        else if (defender.playerCards[num - 1].Suit == royalSuit && card.Suit != royalSuit)
                        { cards_to_delete.Add(card); LogToFile("Карта бита" + '\n'); defender.playerCards.RemoveAt(num - 1); }//карта на столе не козырная, бьём козырной
                        else LogToFile("Карта не бита" + '\n');
                    }
                }

                //если все карты биты, то очищаем стол
                if (cards_to_delete.Count == cardsOnTable.Count + thrown_cards.Count()) cardsOnTable.Clear();
                //иначе, добавляем игроку все карты
                else
                {
                    defender.playerCards.AddRange(cardsOnTable);
                    defender.playerCards.AddRange(cards_to_delete);
                    defender.playerCards.AddRange(thrown_cards);
                    cardsOnTable.Clear();
                }

            }

            // если защищается компьютер
            if (defender is Computer)
            {
                Random random = new Random();
                int num = random.Next(0, 3); // с вероятностью 1 к 3 компьютер заберет козырные карты себе

                // компьютер забирает карты
                if (num == 0 && cardsOnTable.Where(c => c.Suit == royalSuit).Count() > 0)
                {
                    defender.playerCards.AddRange(cardsOnTable);
                    cardsOnTable.Clear();
                    return;
                }

                // карты компьютера, которыми он бил карты на столе
                // если компьютер не сможет побить карты на столе, то они отходят к компьютеру
                List<Card> cards_to_delete = new List<Card>();

                // проходим по каждой карте на столе и бьём её
                foreach (Card card in cardsOnTable)
                {
                    Card c_card; //выбираем карту, которой будем бить
                    if (defender.playerCards.Where(c => c.Suit == card.Suit && c.Power > card.Power).Count() > 0)
                    {//карты одинаковой масти, карта большего ранга, чем на столе - выбираем минимальную подходящую
                        c_card = defender.playerCards.Where(c => c.Suit == card.Suit && c.Power > card.Power).OrderBy(c => c.Power).ToList()[0];
                        LogToFile("Карта бита. Использована карта " + c_card.Suit + ' ' + c_card.Power + '\n');
                        defender.playerCards.Remove(c_card);
                        cards_to_delete.Add(c_card);
                    }
                    else if (defender.playerCards.Where(c => c.Suit == royalSuit && card.Suit != royalSuit).Count() > 0)
                    {//бьём минимальным козырем карту другой масти
                        c_card = defender.playerCards.Where(c => c.Suit == royalSuit && card.Suit != royalSuit).OrderBy(c => c.Power).ToList()[0];
                        LogToFile("Карта бита. Использована карта " + c_card.Suit + ' ' + c_card.Power + '\n');
                        defender.playerCards.Remove(c_card);
                        cards_to_delete.Add(c_card);
                    }
                    else LogToFile("Карта не бита");
                }

                List<Card> thrown_cards = new List<Card>(); //подкинутые карты
                LogToFile("1. Подбросить карты\n2. Не подкидывать" + '\n');
                num = int.Parse(Console.ReadLine());

                // Подбрасываем карты
                // подбрасывать можно все карты того же ранга, которые участвуют в данном заходе:
                // как те, которыми атакуют, так и те, которыми отбиваются;
                if (num != 2 && attacker.playerCards
                    .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power).Contains(c.Power)).Count() > 0)
                {
                    num = 1;
                    for (int i = 0; i < 5 && i < defender.playerCards.Count(); i++)
                    {
                        int j = 0;
                        LogToFile("Подбросить можно одну из: " + '\n');
                        attacker.playerCards
                            .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power)
                            .Contains(c.Power))
                            .ToList()
                            .ForEach(c => { j++; LogToFile(j + ". " + c.Suit + ' ' + c.Power + ' '); });
                        LogToFile("\nЕсли вы не хотите подбрасывать карту, нажмите 0" + '\n');

                        // номер подрошенной карты
                        num = int.Parse(Console.ReadLine());
                        if (num == 0) break;

                        // подкидываем карту
                        thrown_cards.Add(attacker.playerCards
                            .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power)
                            .Contains(c.Power))
                            .ToList()[num - 1]);
                        attacker.playerCards.Remove(attacker.playerCards                                                 //<----------------
                            .Where(c => c.Power == cardsOnTable[0].Power || cards_to_delete.ConvertAll(c => c.Power)
                            .Contains(c.Power))
                            .ToList()[num - 1]);
                    }
                }

                //если есть подкинутые карты
                if (thrown_cards.Count > 0)
                {
                    LogToFile("Подкинуты карты:" + '\n');
                    int i = 0;
                    thrown_cards.ForEach(c => { i++; LogToFile(i + ". " + c.Suit + ' ' + c.Power + '\n'); });

                    // бьем подкинутые карты
                    foreach (Card card in thrown_cards)
                    {
                        Card c_card; //выбираем карту, которой будем бить

                        // Карты одинаковой масти, карта большего ранга, чем на столе - выбираем минимальную подходящую
                        if (defender.playerCards.Where(c => c.Suit == card.Suit && c.Power > card.Power).Count() > 0)
                        {
                            c_card = defender.playerCards.Where(c => c.Suit == card.Suit && c.Power > card.Power).OrderBy(c => c.Power).ToList()[0];
                            LogToFile("Карта " + card.Suit + ' ' + card.Power + "бита. Использована карта " + c_card.Suit + ' ' + c_card.Power + '\n');
                            defender.playerCards.Remove(c_card);
                            cards_to_delete.Add(c_card);
                        }
                        // Бьём минимальным козырем карту другой масти
                        else if (defender.playerCards.Where(c => c.Suit == royalSuit && card.Suit != royalSuit).Count() > 0)
                        {
                            c_card = defender.playerCards.Where(c => c.Suit == royalSuit && card.Suit != royalSuit).OrderBy(c => c.Power).ToList()[0];
                            LogToFile("Карта " + card.Suit + ' ' + card.Power + "бита. Использована карта " + c_card.Suit + ' ' + c_card.Power + '\n');
                            defender.playerCards.Remove(c_card);
                            cards_to_delete.Add(c_card);
                        }
                        else LogToFile("Карта " + card.Suit + ' ' + card.Power + "не бита" + '\n');
                    }
                }
                // Если все карты биты, то очищаем стол
                if (cards_to_delete.Count == cardsOnTable.Count + thrown_cards.Count()) cardsOnTable.Clear();
                // Иначе, добавляем игроку все карты
                else
                {
                    defender.playerCards.AddRange(cardsOnTable);
                    defender.playerCards.AddRange(cards_to_delete);
                    defender.playerCards.AddRange(thrown_cards);
                    cardsOnTable.Clear();
                }

            }
        }

        // абстрактный класс для человека
        public abstract class Player
        {
            public string Name { get; private set; }

            public abstract void DisplayCards();

            public List<Card> playerCards = new List<Card>(6);

            public int PlayerOrder { get; set; }

            public Player(string name)
            {
                Name = name;
            }

            // получения ранга меньшей козырной карты
            // для определения того, кто ходит первым
            public int MinRoyalCard()
            {
                int min = 15;
                foreach (Card card in playerCards)
                {
                    if (card.Suit == royalSuit && card.Power < min)
                    {
                        min = card.Power;
                    }
                }
                return min;
            }

        }

        // Класс для человека
        public class Human : Player
        {
            //показать игроку его карты для выбора
            public override void DisplayCards()
            {
                int i = 0;
                foreach (Card card in playerCards)
                {
                    i++;
                    LogToFile(i + ". " + card.Suit + " " + card.Power + "   ");
                }
            }

            public Human(string name) : base(name) { }
        }

        // Класс для компьютера
        public class Computer : Player
        {
            public override void DisplayCards()
            {
                playerCards.ForEach(c => LogToFile(c.Suit + " " + c.Power + '\n'));
            }

            public Computer(string name) : base(name) { }
        }
    }
}