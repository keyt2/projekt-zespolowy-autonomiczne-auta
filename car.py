import geopandas as gpd
import osmnx as ox
import networkx as nx


class Car:
    def __init__(self, car_id: int, capacity: int, battery_time: float, graph):
        self.car_id = car_id
        self.capacity = capacity
        self.battery_time = battery_time
        self.route = []
        self.street_length_travelled = 0
        self.current_node = 0
        self.graph = graph
        # każde auto ma przypisaną do siebie drogę, którą ma przejechać w postaci listy węzłów;
        # ta lista węzłów jest zapisana w route, a current_street przechowuje aktualną krawędź,
        # na której jest auto
        self.current_street = " "

    # przyjęłam, że trasę będziemy przypisywać nie przy tworzeniu auta, ale przez oddzielną metodę
    def set_route(self, route):
        self.route = route
        self.current_node = 0
        self.current_street = self.graph[route[self.current_node]][route[self.current_node + 1]]

    def show_statistics(self):
        # jeżeli auto ma akurat przypisaną jakąś prośbę, to jego statystyki wyglądają tak...
        if (self.current_street != " "):
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
        if self.current_node >= len(self.route) - 1 or self.route == None:
            pass
        # jeśli autko przejechało już długość większą od długości węzła, na którym się znajduje, to przechodzimy
        # do następnego węzła z route
        elif self.current_street[0]['length'] <= self.street_length_travelled:
            self.battery_time -= 0.01
            self.current_node += 1
            self.street_length_travelled = self.street_length_travelled - self.current_street[0]['length']
            print(f'current node: {self.current_node}, number of nodes: {len(self.route)}')
            if self.current_node >= len(self.route) - 1:
                pass
            else:
                self.current_street = self.graph[self.route[self.current_node]][self.route[self.current_node + 1]]
        # jeśli nic z powyższych nie zachodzi, to autko przejeżdża 10 (metrów?) na krawędzi, na której się znajduje
        else:
            self.battery_time -= 0.01
            self.street_length_travelled += 10
