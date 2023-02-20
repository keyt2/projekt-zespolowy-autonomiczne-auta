import copy
import networkx as nx
import osmnx as ox
import datetime

def ramove_car_with_request(fleet, removed_cars):
    for i in range(len(fleet)):
        if len(fleet[i].route) == 0:
            pass
        else:
            removed_cars.append(fleet[i])
            fleet[i] = "no"

def remove_car_with_to_low_battery(battery_cost, fleet, removed_cars):
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        elif fleet[i].battery_time > battery_cost:
            pass
        else:
            removed_cars.append(fleet[i])
            fleet[i] = "no"

def create_dict_distance_from_starting(car_dict, fleet, graph, orig_node_id):
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        elif fleet[i].nearest_node != "":
            # potrzebuje żeby nearest_node było w formie id tego węzła
            nearest_node_id = ox.nearest_nodes(graph, fleet[i].nearest_node['geometry'].centroid.x,
                                               fleet[i].nearest_node['geometry'].centroid.y)
            to_start_length = nx.shortest_path_length(G=graph, source=nearest_node_id, target=orig_node_id,
                                                      weight="length")
            car_dict[fleet[i].car_id] = to_start_length

def sort_dict(car_dict):
    sorted_dict = sorted(car_dict.items(), key=lambda x: x[1])
    sorted_dict = dict(sorted_dict)
    return sorted_dict

def create_dict_final_time(car_dict_real_time, car_dict_time, tm):
    # dodaje do aktualnego czasu
    for key in car_dict_time:
        minutes = car_dict_time[key]
        delta = datetime.timedelta(minutes=minutes)  # najpierw zamieniam minuty na format datetime, w którym jest tm
        car_dict_real_time[key] = tm + delta

def remove_cars_low_battery(bad_id, car_dict_battery, car_dict_time, fleet):
    for key in car_dict_battery:
        if fleet[key].battery_time < car_dict_battery[key]:
            bad_id.append(key)
    for car_id in bad_id:
        car_dict_time.pop(car_id)

def create_dict_battery_cost(battery_cost, car_dict_battery, car_dict_time):
    for key in car_dict_time:
        car_dict_battery[key] = (car_dict_time[key] * 0.01) + battery_cost

def create_dict_time_to_pass_requests(car_dict, car_dict_time):
    # dziele długość trasy przez 10 dla każdego auta (w ciągu jednej minuty przejeżdża 10m)
    for key in car_dict:
        car_dict_time[key] = car_dict[key] / 10

def create_dict_sum_route(car_dict, fleet, graph, orig_node_id):
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        else:
            sum_distance = 0
            # potrzebuje żeby nearest_node było w formie id tego węzła
            geometry = fleet[i].nearest_node.get("geometry")
            # jeśli tego nie sprawdzam to wywala błędy i program ale nie wiem jak pozbyć się tego błędu
            if geometry is None:
                pass
            else:
                nearest_node_id = ox.nearest_nodes(graph, fleet[i].nearest_node['geometry'].centroid.x,
                                                   fleet[i].nearest_node['geometry'].centroid.y)
                sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=nearest_node_id,
                                                                      target=fleet[i].route[1][0][
                                                                          len(fleet[i].route[1][0]) - 1],
                                                                      weight="length")  # pierwsza trasa, aktualna trasa
                j = 2
                dlugosc_route = len(fleet[i].route)
                while j <= dlugosc_route:  # leci po każdej dodanej trasie
                    sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=fleet[i].route[j][0][0],
                                                                          target=fleet[i].route[j][0][
                                                                              len(fleet[i].route[j][0]) - 1],
                                                                          weight="length")
                    j = j + 1
                # dodaje jeszcze odległość ostatniego węzła w route od punktu początkowego w prośbie
                sum_distance = sum_distance + nx.shortest_path_length(G=graph, source=fleet[i].route[j - 1][0][
                    len(fleet[i].route[j - 1][0]) - 1], target=orig_node_id, weight="length")
                car_dict[fleet[i].car_id] = sum_distance

def check_cars(fleet, good_car):
    for i in range(len(fleet)):
        if fleet[i] == "no":
            pass
        else:
            good_car = "Yes"
    return good_car

def remove_car_with_too_low_capacity(fleet, passengers, removed_cars):
    for i in range(len(fleet)):
        if fleet[i].passengers_on_route + passengers <= fleet[i].capacity:
            pass
        else:
            removed_cars.append(fleet[i])
            fleet[i] = "no"

# W przypadku kiedy żadne auto nie jest w stanie przyjąć prośby funkcja zwraca car_id równe 99.
def allocation_request(car_list, route, route_cost, graph, orig_node_id, tak, tm, passengers):
    # tworze oddzielną liste, która jest identyczna jak car_list
    fleet = copy.copy(car_list)
    # policzone z proporcji: przy przejechaniu 10m rozładowuje sie 0,01 czegoś
    battery_cost = (route_cost * 0.01) / 10
    removed_cars = []  # lista odrzuconych aut, to na wypadek jakby w głównej liście nie zostało żadne auto

    # wyklucza auta które już mają przypisaną prośbę
    ramove_car_with_request(fleet, removed_cars)
    # odrzuca auta które nie dojechałyby do celu
    remove_car_with_to_low_battery(battery_cost, fleet, removed_cars)

    # teraz posortuje listę tak żeby na początku były auta które są najbliżej punktu startowego
    while tak != 21:
        chosen_car_id = tak
        tak += 1
        return tak, chosen_car_id

    #tworze słownik car_id : odleglość od punktu startowego w trasie
    car_dict = {}
    create_dict_distance_from_starting(car_dict, fleet, graph, orig_node_id)
    # sortuje po odległości rosnąco
    sorted_dict = dict()
    sorted_dict = sort_dict(car_dict)
    # w idealnym przypadku mam coś na tej liście więc wybieram pierwszego, który jest najbliżej
    if len(sorted_dict) != 0:
        chosen_car_id = list(sorted_dict.keys())[0]
        return tak, chosen_car_id
    else:                                             #to znaczy że wszystkie auta miały jakąś prośbe
        fleet = copy.copy(removed_cars)
        removed_cars.clear()

    # odrzucam te auta w których nie zmieściłaby się wystaraczająca ilość osób
    remove_car_with_too_low_capacity(fleet, passengers, removed_cars)
    #trzeba sprawdzić czy jakiekolwiek auto da radę zabrać wszystkich z prośby
    good_car = "No"
    good_car = check_cars(fleet, good_car)
    if good_car == "No":
        chosen_car_id = 99
        return tak, chosen_car_id

    #tworze słownik car_id : dłgość wszystkich tras zapisanych obecnie w route dla każdego auta
    car_dict = {}
    create_dict_sum_route(car_dict, fleet, graph, orig_node_id)
    # tworze słownik car_id : czas do przejechania wszystkich próśb
    car_dict_time = {}
    create_dict_time_to_pass_requests(car_dict, car_dict_time)
    # tworze słownik car_id : koszt baterii do przejechania wszystkich próśb + koszt przejechania nowej prośby
    car_dict_battery = {}
    create_dict_battery_cost(battery_cost, car_dict_battery, car_dict_time)

    # teraz odrzucam te auta które mają za mało baterii
    bad_id = []   #lista z car_id, które nie przejadą danej prośby
    remove_cars_low_battery(bad_id, car_dict_battery, car_dict_time, fleet)
    # dodaje samochodom z niską baterią dodaktową trasę po której doładuje im się czas baterii
    for car_id in bad_id:
        car_list[car_id].add_route("ladowanie", 0)

    # tworze słownik car_id : czas w którym skończy obsługiwanie swoich próśb
    car_dict_real_time = {}
    create_dict_final_time(car_dict_real_time, car_dict_time, tm)
    # sortuje po czasie rosnąco
    sorted_dict = dict()
    sorted_dict = sort_dict(car_dict_real_time)

    # w idealnym przypadku mam coś na tej liście więc wybieram pierwszego, który jest najbliżej
    if len(sorted_dict) != 0:
        chosen_car_id = list(sorted_dict.keys())[0]
        return tak, chosen_car_id

    else:                                        #to znaczy że wszystkie auta nie mają baterii żeby dojechać do celu
        chosen_car_id = 99
        return tak, chosen_car_id
