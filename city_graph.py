import matplotlib.pyplot as plt
from pyproj import CRS
from car import Car
import geopandas as gpd
import osmnx as ox
import networkx as nx

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
ox.plot_graph_route(graph, route)

# UWAGA! Tu niżej miał być niby pokazany najbliższy węzeł do Czachowskiego 36. Ale to
# nie jest dobrze zrobione z pewnych względów. Na grafie pokazuje się złe miejsce.
# Przynajmniej widać jakiś punkt.
place = "Czachowskiego 36, Iłża"
position = ox.geocode(place)
nearest_node = ox.nearest_nodes(graph, position[0], position[1])
car_1 = Car(1, 5, graph.nodes[nearest_node]['x'], graph.nodes[nearest_node]['y'], 100, 0, 0, 0, graph)
car_1.show_statistics()
fig, ax = ox.plot_graph(graph, show=False, close=False)
ax.scatter(graph.nodes[nearest_node]['x'], graph.nodes[nearest_node]['y'], c='blue')
plt.show()