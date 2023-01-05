import copy


'''obsługa zapytań
   (na razie dosyć prymitywna ale popracuje jeszcze nad tym aby ją dokończyć
   i wprowadzić większą optymalizację)
   na razie zakładam że zawsze jest jakieś wolne auto bez prośby
'''
def allocation_request(car_list, route, route_cost, tak):
    # tworze oddzielną liste z wyszystkimi autami z której będę kolejno niektóre wykluczać,
    # a na koniec ją posortuje i wybiore najlepsze auto
    fleet = copy.copy(car_list)
    #print(f'dlugosc {route_cost}')           #<- do testów, później zniknie
    # policzone z proporcji: przy przejechaniu 10m rozładowuje sie 0,01 czegoś
    battery_cost = (route_cost * 0.01) / 10
    #print(f'zuzycie baterii {battery_cost}')   #<- do testów później zniknie

    removed_cars = []  # lista odrzuconych aut, to na wypadek jakby w głównej liście nie zostało żadne auto

    # pierwsza pętla wyklucza auta które już mają przypisaną prośbę
    for i in range(len(fleet)):
        if fleet[i].route == []:
            print(f'wolne auto    {fleet[i].car_id}')                     #<- do testów później zniknie
        else:
            removed_cars.append(fleet[i])
            print(f'zajete auto    {fleet[i].car_id}')                    #<- do testów później zniknie
            fleet[i] = "no"  # tymczasowe rozwiązanie, nie wiem jak usunąć elementy z listy tak aby pozostałe zachowały swój indeks, coś wymyśle jeszcze
            # del fleet[i]

    # druga pętla odrzuca auta które nie dojechałyby do celu
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        elif fleet[i].battery_time > battery_cost:
            print(f'dojedzie    {fleet[i].car_id}')                  #<- do testów później zniknie
        else:
            removed_cars.append(fleet[i])
            print(f'za mało baterii    {fleet[i].car_id}')           #<- do testów później zniknie
            fleet[i] = "no"  # tymczasowe rozwiązanie, nie wiem jak usunąć elementy z listy tak aby pozostałe zachowały swój indeks
            # del fleet[i]

    # teraz posortuje listę tak żeby na początku były auta które są najbliżej punktu startowego
        '''
        if current_street == " ": ...

         current_street - aktualna krawędź
         jak wyznaczyć najbliższy wezel??? nearest_node = ???
         chyba najlepiej będzie wyznaczyć najkrótszą trasę od miejsca auta do węzła początkowego   route[0]
         albo jakoś podziałać z węzłami, mam aktualną krawędź auta, ta krawędź przecież ma jakieś węzły 
         nearest_node - route[0] - cos takiego to by była odległość auta od punktu startowego, jeśli ma to jakiś sens
          i jeśli można odejmować od siebie węzły, pewnie nie 

         tak = 'odległość od punktu startowego'
         fleet.sort(key=tak)
         '''

        # w idealnym przypadku mam coś na tej liście więc wybieram pierwszego, który jest najbliżej

        # dobra na razie jeszcze nie wiem jak to zrobić ale wymyśle wkrótce. Wstawiam co mam tak żeby można już było puścić
        # program ktory obsluguje pare prosb. Na razie są one przydzialne każdemu autu po kolei
    fleet[tak].set_route(route)
    print(f'auto ktore dostało prośbe {fleet[tak].car_id}')                   #<- do testów później zniknie
    tak += 1
    return car_list, tak

    # koniec obsługi zapytań
