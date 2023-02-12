import copy
import networkx as nx
import osmnx as ox
import datetime

def allocation_request(car_list, route, route_cost, graph, orig_node_id, tak, tm, passengers):
    # W przypadku kiedy żadne auto nie jest w stanie przyjąć prośby funkcja zwraca car_id równe 99.

    # tworze oddzielną liste, która jest identyczna jak car_list
    fleet = copy.copy(car_list)
    print(f'dlugosc {route_cost}')           #<- do testów, później zniknie
    # policzone z proporcji: przy przejechaniu 10m rozładowuje sie 0,01 czegoś
    battery_cost = (route_cost * 0.01) / 10
    print(f'zuzycie baterii {battery_cost}')   #<- do testów później zniknie

    removed_cars = []  # lista odrzuconych aut, to na wypadek jakby w głównej liście nie zostało żadne auto

    # pierwsza pętla wyklucza auta które już mają przypisaną prośbę
    for i in range(len(fleet)):
        if len(fleet[i].route) == 0:
            print(f'wolne auto    {fleet[i].car_id}')  # <- do testów później zniknie
        else:
            removed_cars.append(fleet[i])
            print(f'zajete auto    {fleet[i].car_id}')  # <- do testów później zniknie
            fleet[i] = "no"  # tymczasowe rozwiązanie, nie wiem jak usunąć elementy z listy tak aby pozostałe zachowały swój indeks, coś wymyśle jeszcze
            # del fleet[i]

    # druga pętla odrzuca auta, które nie dojechałyby do celu
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        elif fleet[i].battery_time > battery_cost:
            print(f'dojedzie    {fleet[i].car_id}')                  #<- do testów później zniknie
        else:
            removed_cars.append(fleet[i])
            print(f'za mało baterii    {fleet[i].car_id}')           #<- do testów później zniknie
            fleet[i] = "no"
            # del fleet[i]

    # teraz posortuje listę tak żeby na początku były auta które są najbliżej punktu startowego
        # zakładam że auto ma jakieś current_street i ma jakieś nearest_node

    # to zapewnia current_street dla aut
    while tak != 5:
        chosen_car_id = tak
        # fleet[tak].add_route(route, passengers)
        print(f'auto ktore dostało prośbe {chosen_car_id}')                   #<- do testów później zniknie
        # chosen_car_id = tak
        tak += 1
        return tak, chosen_car_id



    #tworze słownik car_id : odleglość od punktu startowego w trasie
    car_dict = {}
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        elif fleet[i].nearest_node != "":
            # potrzebuje żeby nearest_node było w formie id tego węzła
            nearest_node_id = ox.nearest_nodes(graph, fleet[i].nearest_node['geometry'].centroid.x, fleet[i].nearest_node['geometry'].centroid.y)
            to_start_length = nx.shortest_path_length(G=graph, source=nearest_node_id, target=orig_node_id, weight="length")
            print(to_start_length)
            car_dict[fleet[i].car_id] = to_start_length

    # sortuje po odległości rosnąco
    sorted_dict = sorted(car_dict.items(), key=lambda x: x[1])
    sorted_dict = dict(sorted_dict)
    print(f'posortowane id:  {sorted_dict}')

    # w idealnym przypadku mam coś na tej liście więc wybieram pierwszego, który jest najbliżej
    if len(sorted_dict) != 0:
        chosen_car_id = list(sorted_dict.keys())[0]
        # fleet[chosen_car_id].add_route(route, passengers)
        # print(f'auto ktore dostało prośbe {fleet[chosen_car_id].car_id}')
        print(f'auto, które dostało prośbę {chosen_car_id}')
        return tak, chosen_car_id

    else:                                             #to znaczy że wszystkie auta miały jakąś prośbe
        fleet = copy.copy(removed_cars)
        removed_cars.clear()


    # na razie zakładam że auto nie bierze nikogo po drodze
    # na początek odrzucam te auta w których nie zmieściłaby się wystaraczająca ilość osób
    for i in range(len(fleet)):
        if fleet[i].passengers_on_route + passengers <= fleet[i].capacity:
            print(f'auto ma wystarczająco dużo miejsca    {fleet[i].car_id}')  # <- do testów później zniknie
        else:
            removed_cars.append(fleet[i])
            print(f'auto nie ma wystarczająco miejsca    {fleet[i].car_id}')  # <- do testów później zniknie
            fleet[i] = "no"
            # del fleet[i]


    #trzeba sprawdzić czy jakiekolwiek auto da radę zabrać wszystkich z prośby
    good_car = "No"
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        else:
            good_car = "Yes"

    if good_car == "No":
        print("Żadne auto nie ma wystarczającej ilości miejsca do zabrania wszystkich pasażerów")
        chosen_car_id = 99
        return tak, chosen_car_id

    #tworze słownik car_id : dłgość wszystkich tras zapisanych obecnie w route dla każdego auta
    car_dict = {}
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        else:
            sum_distance = 0
            # potrzebuje żeby nearest_node było w formie id tego węzła
            geometry = fleet[i].nearest_node.get("geometry")    #jeśli tego nie sprawdzam to wywala błędy i program ale nie wiem jak pozbyć się tego błędu
            if geometry is None:
                pass
            else:
                nearest_node_id = ox.nearest_nodes(graph, fleet[i].nearest_node['geometry'].centroid.x, fleet[i].nearest_node['geometry'].centroid.y)
                sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=nearest_node_id, target=fleet[i].route[1][0][len(fleet[i].route[1][0])-1], weight="length") #pierwsza trasa, aktualna trasa
                j = 2
                dlugosc_route = len(fleet[i].route)
                while j <= dlugosc_route:      #leci po każdej dodanej trasie
                    sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=fleet[i].route[j][0][0], target=fleet[i].route[j][0][len(fleet[i].route[j][0])-1], weight="length")
                    j = j + 1
                # dodaje jeszcze odległość ostatniego węzła w route od punktu początkowego w prośbie
                sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=fleet[i].route[j-1][0][len(fleet[i].route[j-1][0])-1], target=orig_node_id, weight="length")
                print(f'suma trasy jednego auta: {sum_distance}')
                car_dict[fleet[i].car_id] = sum_distance



    # tworze słownik car_id : czas do przejechania wszystkich próśb
    car_dict_time = {}
    # dziele długość trasy przez 10 dla każdego auta (w ciągu jednej minuty przejeżdża 10m)
    for key in car_dict:
        car_dict_time[key] = car_dict[key] / 10

    # tworze słownik car_id : koszt baterii do przejechania wszystkich próśb + koszt przejechania nowej prośby
    car_dict_battery = {}
    for key in car_dict_time:
        car_dict_battery[key] = (car_dict_time[key] * 0.01) + battery_cost

    # teraz odrzucam te auta które mają za mało baterii
    bad_id = []   #lista z car_id, które nie przejadą danej prośby
    for key in car_dict_battery:
        if fleet[key].battery_time < car_dict_battery[key]:
            bad_id.append(key)

    for car_id in bad_id:
        car_dict_time.pop(car_id)

    """Tuta można zrobić wysyłanie tych sałabo naładowanych aut do ładowania, czy tam tankowania"""
    # mam pomysł żeby dodać samochodom z niską baterią dodaktową trasę po której doładuje im się czas baterii
    for car_id in bad_id:
        car_list[car_id].add_route("ladowanie", 0)

    # tworze słownik car_id : czas w którym skończy obsługiwanie swoich próśb
    car_dict_real_time = {}
    #dodaje do aktualnego czasu
    for key in car_dict_time:
        minutes = car_dict_time[key]
        delta = datetime.timedelta(minutes=minutes)     #najpierw zamieniam minuty na format datetime, w którym jest tm
        car_dict_real_time[key] = tm + delta

    # posortować i będzie kto będzie najszybciej
    # sortuje po czasie rosnąco
    sorted_dict = sorted(car_dict_real_time.items(), key=lambda x: x[1])
    sorted_dict = dict(sorted_dict)
    print(f'posortowane id:  {sorted_dict}')

    # w idealnym przypadku mam coś na tej liście więc wybieram pierwszego, który jest najbliżej
    if len(sorted_dict) != 0:
        chosen_car_id = list(sorted_dict.keys())[0]
        # fleet[chosen_car_id].add_route(route, passengers)
        print(f'auto ktore dostało prośbe {chosen_car_id}')
        return tak, chosen_car_id

    else:                                        #to znaczy że wszystkie auta nie mają baterii żeby dojechać do celu
        chosen_car_id = 99
        print("żadne auto nie ma wystarczająco dużo baterii aby przejechać daną trasę")
        return tak, chosen_car_id
