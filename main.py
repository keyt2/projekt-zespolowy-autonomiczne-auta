import time
from datetime import timedelta
from car import Car
import geopandas as gpd
import osmnx as ox
import networkx as nx
from pyproj import CRS
import pandas as pd
from request_generator import RequestGenerator
from request import Request


city_name = "Iłża, Poland"
graph = ox.graph_from_place(city_name, network_type='drive')
nodes, edges = ox.graph_to_gdfs(graph)
placename = "Samodzielny Publiczny Zespół Zakładów Opieki Zdrowotnej - Szpital w Iłży"
geocoded_place = ox.geocode_to_gdf(placename)
geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
origin = geocoded_place["geometry"].centroid.values[0]
placename = "Liceum Ogólnokształcące im. M. Kopernika"
geocoded_place = ox.geocode_to_gdf(placename)
geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
destination = geocoded_place["geometry"].centroid.values[0]
orig_node_id = ox.nearest_nodes(graph, origin.x, origin.y)
target_node_id = ox.nearest_nodes(graph, destination.x, destination.y)
orig_node = nodes.loc[orig_node_id]
target_node = nodes.loc[target_node_id]
od_nodes = gpd.GeoDataFrame([orig_node, target_node], geometry='geometry', crs=nodes.crs)
route = nx.shortest_path(G=graph, source=orig_node_id, target=target_node_id, weight="length")


def main():
    time_in_min = 0  # na razie zakładam, że każdy update w programie będzie oznaczał upływ 1 minuty w świecie realnym
    rg = RequestGenerator()
    r = rg.generate_request()
    r.show()
    geocoded_place = ox.geocode_to_gdf(r.address_from + ", Iłża", which_result=1)
    geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
    origin = geocoded_place["geometry"].centroid.values[0]
    geocoded_place = ox.geocode_to_gdf(r.address_to + ", Iłża", which_result=1)
    geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
    destination = geocoded_place["geometry"].centroid.values[0]
    orig_node_id = ox.nearest_nodes(graph, origin.x, origin.y)
    target_node_id = ox.nearest_nodes(graph, destination.x, destination.y)
    route = nx.shortest_path(G=graph, source=orig_node_id, target=target_node_id, weight="length")
    ox.plot_graph_route(graph, route)
    car1 = Car(1, 5, 5, route, graph)
    car2 = Car(2, 5, 20, route, graph)
    car3 = Car(3, 5, 20, route, graph)
    car4 = Car(4, 5, 20, route, graph)
    car5 = Car(5, 5, 20, route, graph)
    car6 = Car(6, 5, 20, route, graph)
    car7 = Car(7, 5, 20, route, graph)
    car8 = Car(8, 5, 20, route, graph)
    car9 = Car(9, 5, 20, route, graph)
    car10 = Car(10, 5, 25, route, graph)
    car11 = Car(11, 5, 22, route, graph)
    car12 = Car(12, 5, 20, route, graph)
    car13 = Car(13, 5, 21, route, graph)
    car14 = Car(14, 5, 20, route, graph)
    car15 = Car(15, 6, 23, route, graph)
    car16 = Car(16, 5, 20, route, graph)
    car17 = Car(17, 3, 20, route, graph)
    car18 = Car(18, 5, 25, route, graph)
    car19 = Car(19, 6, 20, route, graph)
    car20 = Car(20, 8, 15, route, graph)
    while True:
        time.sleep(0.2)
        time_in_min += 1
        td = timedelta(minutes=time_in_min)
        print('Time in hh:mm:ss:', td)
        car1.update_position()
        car1.show_statistics()
        if time_in_min == 400:
            break


main()
