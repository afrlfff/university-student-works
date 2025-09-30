#include "lib.h"
#include "FundList.h"
#include "ClientsList.h"
#include "func.h"

void Process(FundList* Fund, ClientsList* Clients, fstream* fprotok)
{
    fstream frez;
    Money* mtmp;
    Query* qtmp;
    Client* ctmp;
    FundList FundTmp;
    ClientsList ClientsTmp;
    unsigned maxClients, minRejections;



	*fprotok << "\nШАГ 1. Определим максимальное число клиентов, которых можно обслужить\n"
		<< "	   Для этого переберем все возможные комбинации номиналов в запросах клиентов,\n"
		<< "	   и выберем те комбинации, при которых будет обслужено максимальное число клиентов.\n\n";

    vector<unsigned> queriesN;
    vector<unsigned> queriesTmp, queriesTmp2;
    vector<vector<unsigned>> possible_combinations;
    unsigned maxTmp, minTmp;

    // ФОРМИРУЕМ ВСПОМОГАТЕЛЬНЫЕ СПИСКИ
    ctmp = Clients->get_head();
    while (ctmp != nullptr)
    {
        queriesN.push_back(ctmp->Queries.N);
        queriesTmp.push_back(0);
        ctmp = ctmp->next;
    }

    // ПЕРЕБОР
    maxClients = 0;
    while (queriesTmp != queriesN)
    {
        queriesTmp2 = queriesTmp;
        maxTmp = 0;
        FundTmp = Fund->copy();
        ctmp = Clients->get_head();
        for (unsigned i = 0; i < Clients->N; i++) // рассматриваем данную комбинацию
        {
            qtmp = ctmp->Queries.get_head();
            for (unsigned j = 1; j < queriesTmp[i]; j++) {
                qtmp = qtmp->next;
            }

            // check if qtmp.nominal is in the current Fund
            mtmp = FundTmp.get_element_by_nominal(qtmp->money.nominal);
            if (mtmp->count > 0) {
                FundTmp.change_count(mtmp, -1);
                maxTmp++;
            }
            else
            {
                queriesTmp2[i] = 0;
            }

            ctmp = ctmp->next;
        }
        FundTmp.delete_list();

        if (maxTmp >= maxClients)
        {
            if (maxTmp > maxClients) {
                possible_combinations.clear();
                possible_combinations.push_back(queriesTmp2);
            }
            if (maxTmp == maxClients)
            {
                possible_combinations.push_back(queriesTmp2);
            }
            maxClients = maxTmp;
        }

        for (unsigned i = 0; i < Clients->N; i++) // меняем комбинацию
        {
            queriesTmp[i] += 1;
            if (queriesTmp[i] == queriesN[i] + 1) {
                queriesTmp[i] = 1;
            }
            else break;
        }
    }
    if (possible_combinations.empty())
    {
        possible_combinations.push_back(queriesN);
    }

    *fprotok
        << "Результат:\n"
        << "1.1) Максимальное число обслуженных клиентов: " << maxClients << endl
        << "1.2) Возможные комбинации удовлетворения запросов:\n";
    for (int i = 0; i < possible_combinations.size(); i++) {
        *fprotok << "\ta = [";
        for (int j = 0; j < possible_combinations[i].size(); j++) {
            *fprotok << possible_combinations[i][j];
            if (j == possible_combinations[i].size() - 1)
                *fprotok << "]\n";
            else
                *fprotok << ", ";
        }
    }
    *fprotok << ", где i-й элемент соответствует a[i] запросу i-го клиента,\n"
        << "а \"0\" означает, что данный клиент не рассматривается\n"
        << "(вся нумерация начинается с единицы)\n";




    *fprotok << "\nШАГ 2. Определим минимальное число отказов среди всех запросов.\n"
        << "	   Для этого пройдемся по всем найденным комбинациям запросов и для каждой\n"
        << "	   из них будем удовлетворять все оставшиеся запросы, пока позволяет фонд.\n"
        << "       Таким образом мы найдем минимальное число отказов для данной комбинации,\n"
        << "       после чего нам останется лишь выбрать наиболее оптимальную комбинацию.\n";
    
    vector<vector<unsigned>> final_combinations;
    minRejections = Clients->AllQueriesCount;
    for (unsigned i = 0; i < possible_combinations.size(); i++)
    {
        minTmp = Clients->AllQueriesCount;
        FundTmp = Fund->copy();
        ClientsTmp = Clients->copy();


        // УДОВЛЕТВОРЯЕМ ЗАПРОСЫ ДАННОЙ КОМБИНАЦИИ
        ctmp = ClientsTmp.get_head();
        for (unsigned j = 0; j < ClientsTmp.N; j++)
        {
            if (possible_combinations[i][j] > 0)
            {
                qtmp = ctmp->Queries.get_head();
                for (unsigned k = 1; k < possible_combinations[i][j]; k++) {
                    qtmp = qtmp->next;
                }

                mtmp = FundTmp.get_element_by_nominal(qtmp->money.nominal);
                FundTmp.change_count(mtmp, -1);
                ctmp->Queries.change_count(qtmp, -1);
                minTmp -= 1;
            }

            ctmp = ctmp->next;
        }

        // ОБСЛУЖИВАЕМ ОСТАВШИЕСЯ ЗАПРОСЫ, ПОКА ЭТО ВОЗМОЖНО
        ctmp = ClientsTmp.get_head();
        while (ctmp != nullptr)
        {
            qtmp = ctmp->Queries.get_head();
            while (qtmp != nullptr)
            {
                mtmp = FundTmp.get_element_by_nominal(qtmp->money.nominal);
                if (mtmp != nullptr && mtmp->count > 0)
                {
                    if (mtmp->count >= qtmp->money.count)
                    {
                        minTmp -= qtmp->money.count;
                        FundTmp.change_count(mtmp, -1 * qtmp->money.count);
                        ctmp->Queries.change_count(qtmp, -1 * qtmp->money.count);
                    }
                    else
                    {
                        minTmp -= mtmp->count;
                        ctmp->Queries.change_count(qtmp, -1 * mtmp->count);
                        FundTmp.delete_element(mtmp);
                    }
                }

                qtmp = qtmp->next;
            }

            ctmp = ctmp->next;
        }
        FundTmp.delete_list();
        ClientsTmp.delete_list();

        // ФИКСИРУЕМ ИЛИ НЕ ФИКСИРУЕМ ДАННУЮ КОМБИНАЦИЮ
        if (minTmp <= minRejections)
        {
            if (minTmp < minRejections)
            {
                final_combinations.clear();
                final_combinations.push_back(possible_combinations[i]);
            }
            else
            {
                final_combinations.push_back(possible_combinations[i]);
            }
            minRejections = minTmp;
        }
    }

    *fprotok
        << "Результат:\n"
        << "2.1) Минимальное число отказов: " << minRejections << endl
        << "2.2) Комбинации, удовлетворяющие этому условию:\n";
    for (int i = 0; i < final_combinations.size(); i++) {
        *fprotok << "\ta = [";
        for (int j = 0; j < final_combinations[i].size(); j++) {
            *fprotok << final_combinations[i][j];
            if (j == final_combinations[i].size() - 1)
                *fprotok << "]\n";
            else
                *fprotok << ", ";
        }
    }
    *fprotok << "(если комбинаций несоклько, программой будет выбрана первая)\n";

    *fprotok << "\nШАГ 3. Теперь, когда найдена итоговая комбинация удовлетворения запросов,\n"
        << "	   при которой будут соблюдены условия задачи, мы повторим с ней те же действия,\n"
        << "	   что и в ШАГЕ 2, и зафиксируем оставшийся фонд, а также клиентов и их запросы\n\n";

    ClientsTmp = Clients->copy(); // для формирования списка всех отказов
                                  // т.к. далее список Clients будет меняться

    // УДОВЛЕТВОРЯЕМ ЗАПРОСЫ ИТОГОВОЙ КОМБИНАЦИИ
    ctmp = Clients->get_head();
    for (unsigned j = 0; j < Clients->N; j++)
    {
        if (final_combinations[0][j] > 0)
        {
            qtmp = ctmp->Queries.get_head();
            for (unsigned k = 1; k < final_combinations[0][j]; k++) {
                qtmp = qtmp->next;
            }

            mtmp = Fund->get_element_by_nominal(qtmp->money.nominal);
            Fund->change_count(mtmp, -1);
            ctmp->Queries.change_count(qtmp, -1);
        }
        ctmp = ctmp->next;
    }
    
    // УДОВЛЕТВОРЯЕМ ОСТАВШИЕСЯ ЗАПРОСЫ, ПОКА ЭТО ВОЗМОЖНО
    ctmp = Clients->get_head();
    while (ctmp != nullptr)
    {
        qtmp = ctmp->Queries.get_head();
        while (qtmp != nullptr)
        {
            mtmp = Fund->get_element_by_nominal(qtmp->money.nominal);
            if (mtmp != nullptr && mtmp->count > 0)
            {
                if (mtmp->count >= qtmp->money.count)
                {
                    Fund->change_count(mtmp, -1 * qtmp->money.count);
                    ctmp->Queries.change_count(qtmp, -1 * qtmp->money.count);
                }
                else
                {
                    ctmp->Queries.change_count(qtmp, -1 * mtmp->count);
                    Fund->delete_element(mtmp);
                }
            }
            qtmp = qtmp->next;
        }
        ctmp = ctmp->next;
    }
    Clients->refresh_data();

    // ФОРМИРУЕМ СПИСОК ВСЕХ ОТКАЗОВ
    Client* ctmp2,*ctmp3;
    Query* qtmp2, *qtmp3;

    ctmp = Clients->get_head();
    ctmp2 = ClientsTmp.get_head();
    while (ctmp != nullptr)
    {
        if (ctmp->Name == ctmp2->Name)
        {
            if (ctmp->Queries == ctmp2->Queries)
            {
                ctmp = ctmp->next;
                ctmp3 = ctmp2;
                ctmp2 = ctmp2->next;
                ClientsTmp.delete_element(ctmp3);
            }
            else
            {
                qtmp = ctmp->Queries.get_head();
                qtmp2 = ctmp2->Queries.get_head();
                while (qtmp2 != nullptr)
                {
                    if (qtmp2->money.nominal != qtmp->money.nominal)
                    {
                        qtmp2 = qtmp2->next;
                    }
                    else
                    {
                        if (qtmp2->money.count != qtmp->money.count)
                        {
                            qtmp2->money.count -= qtmp->money.count;
                        }
                        else
                        {
                            qtmp = qtmp->next;
                            qtmp3 = qtmp2;
                            qtmp2 = qtmp2->next;
                            ctmp2->Queries.delete_element(qtmp3);
                        }
                    }
                }
                ctmp = ctmp->next;
                ctmp2 = ctmp2->next;
            }
        }
        else
        {
            ctmp2 = ctmp2->next;
        }
    }
    *fprotok << "\nПРОГРАММА ЗАВЕРШЕНА. ИТОГОВЫЙ ОТВЕТ В ФАЙЛЕ result.txt\n";


    // ЗАПИСЬ РЕЗУЛЬТАТА
    frez.open("result.txt", ios::out);

    if (Clients->get_head() == nullptr)
    {
        frez << "Запросы всех клиентов удовлетворены.\n"
            << "ОСТАВШИЙСЯ ФОНД:\n"; Fund->out_list(&frez);
    }
    else
    {
        frez << "Запросы всех клиентов удовлетворить не удалось.\n"
            << "Максимальное число обслуженных клиентов: " << maxClients << endl
            << "Минимальное число отказов в запросах: " << minRejections << endl
            << "\nОСТАВШИЙСЯ ФОНД:\n"; Fund->out_list(&frez);
        frez << "\nСПИСОК УДОВЛЕТВОРЕННЫХ ЗАПРОСОВ:\n"; ClientsTmp.out_list(&frez);
        frez << "\nСПИСОК ОСТАВШИХСЯ КЛИЕНТОВ:\n"; Clients->out_list(&frez);
    }

    ClientsTmp.delete_list();
    frez.close();
}