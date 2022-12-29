import random
import time
from datetime import timedelta
from car import Car
#from cars import Cars
import geopandas as gpd
import osmnx as ox
import networkx as nx
from pyproj import CRS
import pandas as pd
from request_generator import RequestGenerator
from request import Request
from PyQt5 import uic, QtWidgets"""to bedzie do GUI"""


#update wszystkich pozycji i statystyk samochodów naraz
def update_all(car_list):
    for i in range(0, 21):
        car_list[i].update_position()
        car_list[i].show_statistics()

def main():
    city_name = "Iłża, Poland"
    graph = ox.graph_from_place(city_name, network_type='drive') # pobieram graf Iłży z przejezdnymi ulicami
    nodes, edges = ox.graph_to_gdfs(graph) # nodes przechowują węzły grafu, edges krawędzie
    time_in_min = 0  # na razie zakładam, że każdy update w programie będzie oznaczał upływ 1 minuty w świecie realnym
    rg = RequestGenerator()
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
    while True:
        time.sleep(0.2)
        time_in_min += 1
        td = timedelta(minutes=time_in_min)
        print('Time in hh:mm:ss:', td)
        # przyjęłam, że jest 1/50 szansy, że w każdej minucie dnia wpłynie jakaś prośba
        if (random.randint(1, 50) == 1):
            r = rg.generate_request() # pobieram prośbę z generatora próśb
            r.show() # pokazuję, jaka prośba (skąd jedziemy i dokąd) została wygenerowana)
            # poniższe trzy linijki: robię jakieś przekształcenia, których sama do końca nie rozumiem, jeżeli chcecie znać szczegóły,
            # to przeanalizujcie ten kurs, który wam wysłałam na GitHubie; generalnie biorę punkt wyjściowy (origin),
            # jakoś go przekształcam do odpowiedniego systemu koordynatów (crs to jest coordinate reference system),
            # i to centroid values bierze środek tego budynku, z którego adresu startujemy;
            # jeżeli chcecie szczegółów, to musicie poczytać dokumentację
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
            ox.plot_graph_route(graph, route)# pokazuje graf(?)
            # jeżeli wpłynęła jakaś prośba, to przypisuję ją do losowego auta; ale to jest rozwiązanie tymczasowe!
            # oczywiście trzeba to pozmieniać, bo w tym momencie auto może porzucić swoją dotychczasową prośbę
            # i przeteleportować się do punktu wyjściowego nowej prośby, co jest oczywiście nierealne
            random.choice(car_list).set_route(route)
        # update_position() służy do tego, żeby autko przesunęło się do przypisanej do niego drodze;
        # show_statistics() pokazuje, gdzie się obecnie znajduje
        update_all(car_list)
        if time_in_min == 400:
            break


main()
