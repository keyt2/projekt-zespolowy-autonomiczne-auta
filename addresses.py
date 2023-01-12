import osmnx as ox
from osmnx import utils_geo
import pandas as pd
import numpy as np

class Addresses:
    city_name = "Iłża, Poland"
    graph = ox.graph_from_place(city_name, network_type='drive')  # pobieram graf Iłży z przejezdnymi ulicami
    residential_area1 = utils_geo.bbox_from_point(ox.geocode("Czachowskiego 41, Iłża"), dist=400)
    # residential_area1 = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3])
    residential_area2 = utils_geo.bbox_from_point(ox.geocode("Zawady 5, Iłża"), dist=500)
    # residential_area2 = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3])
    residential_area3 = utils_geo.bbox_from_point(ox.geocode("Przy Malenie 2A, Iłża"), dist=1500)
    # residential_area3 = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3])
    residential_areas = [residential_area1, residential_area2, residential_area3]
    residential = np.array([])
    for i in residential_areas:
        addresses = pd.DataFrame(
            ox.geometries_from_bbox(i[0], i[1], i[2], i[3], tags={'addr:street': True, 'addr:housenumber': True}))
        addresses = np.column_stack((addresses.loc[:, 'addr:street'], addresses.loc[:, 'addr:housenumber']))
        addresses = np.array(addresses, dtype=str)
        addresses = addresses[~np.any(addresses == 'nan', axis=1)]
        addresses = np.unique(addresses, axis=0)
        if np.size(residential) != 0:
            residential = np.concatenate([residential, addresses])
        else:
            residential = addresses
    residential = np.unique(residential, axis=0)

    city_centre = utils_geo.bbox_from_point(ox.geocode("Kościół pw. Wniebowzięcia Najświętszej Maryi Panny, Iłża"),
                                            dist=300)
    city_centre = pd.DataFrame(ox.geometries_from_bbox(city_centre[0], city_centre[1], city_centre[2], city_centre[3], tags={'addr:street': True, 'addr:housenumber': True}))
    city_centre = np.column_stack((city_centre.loc[:, 'addr:street'], city_centre.loc[:, 'addr:housenumber']))
    city_centre = np.array(city_centre, dtype=str)
    city_centre = city_centre[~np.any(city_centre == 'nan', axis=1)]
    city_centre = np.unique(city_centre, axis=0)

    # city_centre = ox.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3])
    all_addr = pd.DataFrame(ox.geometries_from_place(city_name, tags={'addr:street': True, 'addr:housenumber': True}))
    all_addr = np.column_stack((all_addr.loc[:, 'addr:street'], all_addr.loc[:, 'addr:housenumber']))
    all_addr = np.array(all_addr, dtype=str)
    all_addr = all_addr[~np.any(all_addr == 'nan', axis=1)]
    all_addr = np.unique(all_addr, axis=0)

    shops = pd.DataFrame(ox.geometries_from_place(city_name, tags={
        'shop': ['supermarket', 'convenience', 'department_store', 'mall']}))
    shops = np.column_stack((shops.loc[:, 'addr:street'], shops.loc[:, 'addr:housenumber']))
    shops = np.array(shops, dtype=str)
    shops = shops[~np.any(shops == 'nan', axis=1)]
    shops = np.unique(shops, axis=0)

    schools = pd.DataFrame(ox.geometries_from_place(city_name, tags={'building': 'school'}))
    schools = np.column_stack((schools.loc[:, 'addr:street'], schools.loc[:, 'addr:housenumber']))
    schools = np.array(schools, dtype=str)
    schools = schools[~np.any(schools == 'nan', axis=1)]
    schools = np.unique(schools, axis=0)