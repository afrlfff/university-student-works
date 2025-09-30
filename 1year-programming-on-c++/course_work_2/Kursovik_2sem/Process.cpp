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



	*fprotok << "\n��� 1. ��������� ������������ ����� ��������, ������� ����� ���������\n"
		<< "	   ��� ����� ��������� ��� ��������� ���������� ��������� � �������� ��������,\n"
		<< "	   � ������� �� ����������, ��� ������� ����� ��������� ������������ ����� ��������.\n\n";

    vector<unsigned> queriesN;
    vector<unsigned> queriesTmp, queriesTmp2;
    vector<vector<unsigned>> possible_combinations;
    unsigned maxTmp, minTmp;

    // ��������� ��������������� ������
    ctmp = Clients->get_head();
    while (ctmp != nullptr)
    {
        queriesN.push_back(ctmp->Queries.N);
        queriesTmp.push_back(0);
        ctmp = ctmp->next;
    }

    // �������
    maxClients = 0;
    while (queriesTmp != queriesN)
    {
        queriesTmp2 = queriesTmp;
        maxTmp = 0;
        FundTmp = Fund->copy();
        ctmp = Clients->get_head();
        for (unsigned i = 0; i < Clients->N; i++) // ������������� ������ ����������
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

        for (unsigned i = 0; i < Clients->N; i++) // ������ ����������
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
        << "���������:\n"
        << "1.1) ������������ ����� ����������� ��������: " << maxClients << endl
        << "1.2) ��������� ���������� �������������� ��������:\n";
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
    *fprotok << ", ��� i-� ������� ������������� a[i] ������� i-�� �������,\n"
        << "� \"0\" ��������, ��� ������ ������ �� ���������������\n"
        << "(��� ��������� ���������� � �������)\n";




    *fprotok << "\n��� 2. ��������� ����������� ����� ������� ����� ���� ��������.\n"
        << "	   ��� ����� ��������� �� ���� ��������� ����������� �������� � ��� ������\n"
        << "	   �� ��� ����� ������������� ��� ���������� �������, ���� ��������� ����.\n"
        << "       ����� ������� �� ������ ����������� ����� ������� ��� ������ ����������,\n"
        << "       ����� ���� ��� ��������� ���� ������� �������� ����������� ����������.\n";
    
    vector<vector<unsigned>> final_combinations;
    minRejections = Clients->AllQueriesCount;
    for (unsigned i = 0; i < possible_combinations.size(); i++)
    {
        minTmp = Clients->AllQueriesCount;
        FundTmp = Fund->copy();
        ClientsTmp = Clients->copy();


        // ������������� ������� ������ ����������
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

        // ����������� ���������� �������, ���� ��� ��������
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

        // ��������� ��� �� ��������� ������ ����������
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
        << "���������:\n"
        << "2.1) ����������� ����� �������: " << minRejections << endl
        << "2.2) ����������, ��������������� ����� �������:\n";
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
    *fprotok << "(���� ���������� ���������, ���������� ����� ������� ������)\n";

    *fprotok << "\n��� 3. ������, ����� ������� �������� ���������� �������������� ��������,\n"
        << "	   ��� ������� ����� ��������� ������� ������, �� �������� � ��� �� �� ��������,\n"
        << "	   ��� � � ���� 2, � ����������� ���������� ����, � ����� �������� � �� �������\n\n";

    ClientsTmp = Clients->copy(); // ��� ������������ ������ ���� �������
                                  // �.�. ����� ������ Clients ����� ��������

    // ������������� ������� �������� ����������
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
    
    // ������������� ���������� �������, ���� ��� ��������
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

    // ��������� ������ ���� �������
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
    *fprotok << "\n��������� ���������. �������� ����� � ����� result.txt\n";


    // ������ ����������
    frez.open("result.txt", ios::out);

    if (Clients->get_head() == nullptr)
    {
        frez << "������� ���� �������� �������������.\n"
            << "���������� ����:\n"; Fund->out_list(&frez);
    }
    else
    {
        frez << "������� ���� �������� ������������� �� �������.\n"
            << "������������ ����� ����������� ��������: " << maxClients << endl
            << "����������� ����� ������� � ��������: " << minRejections << endl
            << "\n���������� ����:\n"; Fund->out_list(&frez);
        frez << "\n������ ��������������� ��������:\n"; ClientsTmp.out_list(&frez);
        frez << "\n������ ���������� ��������:\n"; Clients->out_list(&frez);
    }

    ClientsTmp.delete_list();
    frez.close();
}