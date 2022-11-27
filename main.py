import time
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
    while True:
        time.sleep(0.2)
        time_in_min += 1
        car1.update_position()
        car1.show_statistics()
        if time_in_min == 400:
            break


main()
