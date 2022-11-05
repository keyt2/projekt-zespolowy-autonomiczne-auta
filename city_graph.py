import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
from pyproj import CRS
import contextily as ctx

city_name = "Iłża, Poland"
graph = ox.graph_from_place(city_name, network_type='drive')
ox.plot_graph(graph)
nodes, edges = ox.graph_to_gdfs(graph)
#print(edges['highway'].value_counts())
#plt.show()
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