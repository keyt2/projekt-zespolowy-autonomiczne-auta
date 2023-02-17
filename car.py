import geopandas as gpd
import osmnx as ox
import networkx as nx


class Car:
    def __init__(self, car_id: int, capacity: int, battery_time: float, graph):
        self.car_id = car_id
        self.capacity = capacity
        self.battery_time = battery_time
        # route to słownik, który przechowuje id trasy(klucz), liste zawierającą węzły oraz liczbę pasażerów
        # np 1: ([12328382, 223223223, 32342342, 342434234], 3)
        self.route = dict()
        self.street_length_travelled = 0
        self.current_node = 0
        self.graph = graph
        # każde auto ma przypisaną do siebie drogę, którą ma przejechać w postaci listy węzłów;
        # ta lista węzłów jest zapisana w route, a current_street przechowuje aktualną krawędź,
        # na której jest auto
        self.current_street = " "
        # nearest_node: Ten który został minięty jako ostatni
        self.nearest_node = ""
        self.passengers_on_route = 0        # przechowuje ile pasażerów jest w sumie we wszystkich prośbach przypisanych do auta
        self.passengers_on_current_request = 0   # przechowuje ile pasażerów zamówiło aktualnie obsługiwaną prośbę

    # przyjęłam, że trasę będziemy przypisywać nie przy tworzeniu auta, ale przez oddzielną metodę
    # Funkcja add_route, dodaje trasę do kolejki a set_route ustawia daną trasę jako aktualnie obsługiwaną przez auto
    def set_route(self, route):         # uaktualnia właśnie obsługiwaną trasę
        # self.route = route
        if route == "ladowanie":
            self.battery_time = 20
        else:
            self.current_node = 0
            self.current_street = self.graph[route[1][0][self.current_node]][route[1][0][self.current_node + 1]]
            self.passengers_on_current_request = route[1][1]
            self.nearest_node = self.current_street[0]

    def add_route(self, route, passengers):        # dodaje nową prośbę do route
        self.route[len(self.route) + 1] = (route, passengers)
        self.passengers_on_route += passengers
        if self.current_street == " ":
            self.set_route(self.route)

    def del_route(self):        # usuwa spełnioną prośbę z route i ustawia nową jako aktualną
        del self.route[1]       # i zamienia klucze w słowniku, aby po usunięciu pierwszego z listy reszta
        new_dict = {}           # "przesunęła" się o 1 do przodu.
        for key, value in self.route.items():
            new_key = key - 1
            new_dict[new_key] = value
            self.route = new_dict
        self.set_route(self.route)


    def show_statistics(self):
        # jeżeli auto ma akurat przypisaną jakąś prośbę, to jego statystyki wyglądają tak...
        if (len(self.route) != 0):
            print(f"Car number: {self.car_id}, capacity: {self.capacity} people,"
              f" battery time left: {self.battery_time}, current street: {self.current_street[0]['name']}, "
              f" street length travelled: {self.street_length_travelled}, "
              f"street length: {self.current_street[0]['length']}")
            # ... a tak jeśli nie ma przypisanej żadnej prośby
        else:
            print(f"Car number: {self.car_id}, capacity: {self.capacity} people,"
                  f" battery time left: {self.battery_time}, current street: _, "
                  f" street length travelled: {self.street_length_travelled}, "
                  f"street length: _")

# na razie przy każdym updacie autko przejeżdża sobie 10 metrów i rozładowuje się o 0,01 czegoś
# (dostępny czas jeżdżenia zmniejsza się o minutę)
    def update_position(self):
        # jeśli numer węzła, który aktualnie przekroczyło autko jest większy od liczby węzłów zapisanych w route,
        # lub auto nie ma w ogóle przypisanej żadnej trasy, to nie przechodzimy już do następnej krawędzi
        if self.current_street == " ":
            pass
        elif len(self.route) == 0:
            pass
        elif self.current_node >= len(self.route[1][0]) - 1 or len(self.route) == 0:
            if self.current_node >= len(self.route[1][0]) - 1 and self.route.get(2) is not None:
                self.street_length_travelled = self.street_length_travelled - self.current_street[0]['length']
                self.passengers_on_route -= self.passengers_on_current_request
                self.del_route()
            else:
                pass
        # jeśli autko przejechało już długość większą od długości węzła, na którym się znajduje, to przechodzimy
        # do następnego węzła z route
        elif self.current_street[0]['length'] <= self.street_length_travelled:
            self.battery_time -= 0.01
            self.current_node += 1
            self.street_length_travelled = self.street_length_travelled - self.current_street[0]['length']
            print(f'current node: {self.current_node}, number of nodes: {len(self.route[1][0])}')
            if self.current_node >= len(self.route[1][0]) - 1:
                if self.route.get(2) is not None:
                    self.passengers_on_route -= self.passengers_on_current_request  # jeśli został przekroczony ostatni węzeł to sprawdzam czy jest jakaś kolejna prośba w route
                    self.del_route()                                                # jeśli tak to usuwam zrobioną trasę z początku kolejki i ustawiam kolejną jako ta aktualna
                else:
                    pass
            else:
                self.current_street = self.graph[self.route[1][0][self.current_node]][self.route[1][0][self.current_node + 1]]
                self.nearest_node = self.current_street[0]
        # jeśli nic z powyższych nie zachodzi, to autko przejeżdża 10 (metrów?) na krawędzi, na której się znajduje
        else:
            self.battery_time -= 0.01
            self.street_length_travelled += 10
