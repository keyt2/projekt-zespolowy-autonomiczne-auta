import random
import time
from datetime import datetime, timedelta
import os
from car import Car
import geopandas as gpd
import osmnx as ox
import networkx as nx
from pyproj import CRS
import pandas as pd
from request_generator import RequestGenerator
from request import Request
from osmnx import utils_geo
from Allocation_request import allocation_request

#obsługa nieprzydzielonych wcześniej próśb
def handling_unallocated_request(car_list, graph, tak, tm, unallocated_requests):
    # wywołuje funkcje przydzielania prośby
    tak, chosen_car_id = allocation_request(car_list, unallocated_requests[1][0], unallocated_requests[1][1],
                                            graph, unallocated_requests[1][2], tak, tm, unallocated_requests[1][3])
    if chosen_car_id == 99:
        pass
    else:
        print(f"car with request: {chosen_car_id}")
        car_list[chosen_car_id].add_route(unallocated_requests[1][0],
                                          unallocated_requests[1][3])  # usuwa spełnioną prośbę z unallocates_request
        del unallocated_requests[1]  # i zamienia klucze w słowniku, aby po usunięciu pierwszego z listy reszta
        new_dict = {}  # "przesunęła" się o 1 do przodu.
        for key, value in unallocated_requests.items():
            new_key = key - 1
            new_dict[new_key] = value
            unallocated_requests = new_dict

#update wszystkich pozycji i statystyk samochodów naraz
def update_all(car_list):
    for i in range(0, 21):
        # update_position() służy do tego, żeby autko przesunęło się do przypisanej do niego drodze;
        car_list[i].update_position()
        # show_statistics() pokazuje, gdzie się obecnie znajduje
        car_list[i].show_statistics()

def main():
    city_name = "Iłża, Poland"
    graph = ox.graph_from_place(city_name, network_type='drive') # pobieram graf Iłży z przejezdnymi ulicami
    nodes, edges = ox.graph_to_gdfs(graph) # nodes przechowują węzły grafu, edges krawędzie
    rg = RequestGenerator()
    tm = datetime.strptime("2023-02-01 00:00:00", "%Y-%m-%d %H:%M:%S")
   #tworzenie floty samochodów:
    car_list = []
    for i in range(0, 5):
        car_list.append(Car(i, 5, 20, graph))
    for i in range(5, 10):
        car_list.append(Car(i, 5, 25, graph))
    for i in range(10, 15):
        car_list.append(Car(i, 6, 22, graph))
    for i in range(15, 19):
        car_list.append(Car(i, 6, 20, graph))
    for i in range(19, 21):
        car_list.append(Car(i, 3, 20, graph))
    tak = 0    #zapewnia przydzielenie na początku programu wszystkim autom po jednej prośbie.
    unallocated_requests = dict()      # słownik nieprzydzielonych próśb
    while True:
        update_all(car_list)
        time.sleep(0.2)
        tm += timedelta(minutes=1)
        print('Time:', tm)
        r = rg.generate_request(tm) # pobieram prośbę z generatora próśb
        r.show() # pokazuję, jaka prośba (skąd jedziemy i dokąd) została wygenerowana)
        # jeśli została wygenerowana pusta prośba, przechodzę do kolejnego obrotu pętli, ale najpierw obsługuje jedną prośbę z unalloccated_request
        if (r.address_from == "_ _"):
            if len(unallocated_requests) != 0:
                handling_unallocated_request(car_list, graph, tak, tm, unallocated_requests)
            continue 
        # biorę punkt wyjściowy (origin), przekształcam do odpowiedniego systemu koordynatów (crs to jest coordinate reference system),
        # i to centroid values bierze środek tego budynku, z którego adresu startujemy;
        geocoded_place = ox.geocode_to_gdf(r.address_from + ", Iłża", which_result=1)
        geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
        origin = geocoded_place["geometry"].centroid.values[0]
        # to samo co wyżej robię dla punktu docelowego
        geocoded_place = ox.geocode_to_gdf(r.address_to + ", Iłża", which_result=1)
        geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
        destination = geocoded_place["geometry"].centroid.values[0]
        # w dwóch linijkach niżej wyznaczam najbliższe węzły w grafie dla tych punktów, które wyznaczyłam wyżej
        orig_node_id = ox.nearest_nodes(graph, origin.x, origin.y)
        target_node_id = ox.nearest_nodes(graph, destination.x, destination.y)
        # wyznaczam i wyświetlam najkrótszą drogę od węzła wyjściowego do docelowego
        route = nx.shortest_path(G=graph, source=orig_node_id, target=target_node_id, weight="length")
        ox.plot_graph_route(graph, route)  # pokazuje graf(?)
        # dlugosc trasy w metrach
        route_cost = nx.shortest_path_length(G=graph, source=orig_node_id, target=target_node_id, weight="length")
        # funkcja zwraca chosen_car_id czyli indeks wybranego samochodu
        tak, chosen_car_id = allocation_request(car_list, route, route_cost, graph, orig_node_id, tak, tm, r.passangers)
        if chosen_car_id == 99:
            print("Request is not assigned")
            print("Request added to separate list")
            unallocated_requests[len(unallocated_requests) + 1] = (route, route_cost, orig_node_id, r.passangers)
        else:
            car_list[chosen_car_id].add_route(route, r.passangers)
            print(f"car with request: {chosen_car_id}")


main()
