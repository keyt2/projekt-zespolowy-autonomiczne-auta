import geopandas as gpd
import osmnx as ox
import networkx as nx


class Car:
    def __init__(self, car_id: int, capacity: int, battery_time: float, route, graph):
        self.car_id = car_id
        self.capacity = capacity
        self.battery_time = battery_time
        self.route = route
        self.street_length_travelled = 0
        self.current_node = 0
        self.graph = graph
        self.current_street = graph[route[self.current_node]][route[self.current_node + 1]]

    def show_statistics(self):
        print(f"Car number: {self.car_id}, capacity: {self.capacity} people,"
              f" battery time left: {self.battery_time}, current street: {self.current_street[0]['name']}, "
              f" street length travelled: {self.street_length_travelled}, "
              f"street length: {self.current_street[0]['length']}")

# na razie przy każdym updacie autko przejeżdża sobie 10 metrów i rozładowuje się o 0,01 czegoś
# (dostępny czas jeżdżenia zmniejsza się o minutę)
    def update_position(self):
        self.battery_time -= 0.01
        if self.current_node >= len(self.route) - 1:
            pass
        elif self.current_street[0]['length'] <= self.street_length_travelled:
            self.current_node += 1
            self.street_length_travelled = self.street_length_travelled - self.current_street[0]['length']
            print(f'current node: {self.current_node}, number of nodes: {len(self.route)}')
            if self.current_node >= len(self.route) - 1:
                pass
            else:
                self.current_street = self.graph[self.route[self.current_node]][self.route[self.current_node + 1]]
        else:
            self.street_length_travelled += 10
