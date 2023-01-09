import copy
import networkx as nx
#obsluga zapytan

def allocation_request(car_list, route, route_cost, graph, orig_node_id, tak, td):
    chosen_car_id = 0
    # tworze oddzielną liste z wyszystkimi autami z której będę kolejno niektóre wykluczać,
    # a na koniec ją posortuje i wybiore najlepsze auto
    fleet = copy.copy(car_list)
    print(f'dlugosc {route_cost}')           #<- do testów, później zniknie
    # policzone z proporcji: przy przejechaniu 10m rozładowuje sie 0,01 czegoś
    battery_cost = (route_cost * 0.01) / 10
    print(f'zuzycie baterii {battery_cost}')   #<- do testów później zniknie

    removed_cars = []  # lista odrzuconych aut, to na wypadek jakby w głównej liście nie zostało żadne auto

    # pierwsza pętla wyklucza auta które już mają przypisaną prośbę
    for i in range(len(fleet)):
        if fleet[i].route == []:
            print(f'wolne auto    {fleet[i].car_id}')  # <- do testów później zniknie
        else:
            removed_cars.append(fleet[i])
            print(f'zajete auto    {fleet[i].car_id}')  # <- do testów później zniknie
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
        # zakładam że auto ma jakieś current_street i ma jakieś nearest_node
    '''
    while tak != 5:
        fleet[tak].set_route(route)
        print(f'auto ktore dostało prośbe {fleet[tak].car_id}')                   #<- do testów później zniknie
        chosen_car_id = tak
        tak += 1
        return tak, chosen_car_id
    '''


    #tworze słownik car_id : odleglość od punktu startowego w trasie
    car_dict = {}
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        elif fleet[i].nearest_node != "":
            to_start_lenght = nx.shortest_path_length(G=graph, source=fleet[i].nearest_node, target=orig_node_id, weight="length")
            print(to_start_lenght)
            car_dict[fleet[i].car_id] = to_start_lenght

    # sortuje po odległości rosnąco
    sorted_dict = sorted(car_dict.items(), key=lambda x: x[1])
    sorted_dict = dict(sorted_dict)
    print(f'posortowane id:  {sorted_dict}')

    # w idealnym przypadku mam coś na tej liście więc wybieram pierwszego, który jest najbliżej
    if fleet != []:
        chosen_car_id = list(sorted_dict.keys())[0]
        fleet[chosen_car_id].add_route(route)
        print(f'auto ktore dostało prośbe {fleet[chosen_car_id].car_id}')
        return tak, chosen_car_id

    else:
        fleet = copy.copy(removed_cars)

    #to znaczy że wszystkie auta miały jakąś prośbe
        # na razie zakładam że auto nie bierze nikogo po drodze (to znaczy też że nie muszę sprawdzać czy ktoś się jeszcze zmieści w samochodzie)


    #tworze słownik car_id : dłgość wszystkich tras zapisanych obecnie w route dla każdego auta
    car_dict = {}
    for i in range(len(fleet)):
        sum_distance = 0
        sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=fleet[i].nearest_node, target=fleet[i].route[0][len(route[0])-1], weight="length") #pierwsza trasa
        j = 1
        while fleet[i].route[j] != []:  #albo route[j]!= None    #leci po każdej dodanej trasie
            sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=fleet[i].route[j][0], target=fleet[i].route[j][len(route[j])-1], weight="length")
        print(f'suma trasy jednego auta: {sum_distance}')
        car_dict[fleet[i].car_id] = sum_distance

    # tworze słownik car_id : czas do przejechania wszystkich próśb
    car_dict_time = {}
    # dziele długość trasy przez 10 dla każdego auta (w ciągu jednej minuty przejeżdża 10m)
    for key in car_dict:
        car_dict_time[key] = car_dict[key] / 10

    # tworze słownik car_id : czas w którym skończy obsługiwanie swoich próśb
    car_dict_real_time = {}
    #dodaje do aktualnego czasu
    for key in car_dict_time:
        car_dict_real_time[key] = td + car_dict[key]
    # teraz trzeba dodać jeszcze czas dojechania do punktu początkowego od ostatniego węzła w prośbach,
    # posortować i będzie kto będzie najszybciej,
    # póżniej policzyć któremu starczy baterii i wybrać tego z góry listy
    # potrzebuję pomocy w postawieniu auta na jakiejś drodze przy jego tworzeiu
    # tak żeby na start current_streat oraz nearest_node były zainicjowane,
    # wtedy będzie bajka no i nie wiem czy działa ta lista route jako lista list, a jeśli tak to czy nie pomieszałam z indeksami



    #fleet[tak].set_route(route)
    #print(f'auto ktore dostało prośbe {fleet[tak].car_id}')                   #<- do testów później zniknie

    #chosen_car_id = tak
    #tak += 1
    return tak, chosen_car_id

    # koniec obsługi zapytań
