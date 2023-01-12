import numpy as np
import osmnx.distance
import pandas as pd
from request import Request
import osmnx as ox
import random
from randomtimestamp import random_time
from addresses import Addresses
from pyproj import CRS
from datetime import datetime
import random

class RequestGenerator:
    addr = Addresses()
    def generate_request(self, time=datetime.strptime("00:00:00", "%H:%M:%S")):
        i = random.randint(1, 1000)
        while True:
            if datetime.strptime("07:00:00", "%H:%M:%S") < time < datetime.strptime(
                    "10:00:00", "%H:%M:%S"):
                print("morning")
                # jest 20% szansy, że w każdej minucie rano wpłynie jakaś prośba
                if i in range(201, 1001):
                    return Request("_" + " " + "_", "_" + " " + "_", time, 0)
                # z tego ok. 30% szansy, że prośba będzie z residential do schools
                elif i in range(1, 61):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.schools)
                # z tego ok. 15% szansy, że prośba będzie z residential do city_centre
                elif i in range(61, 91):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.city_centre)
                # z tego ok. 15% szansy, że prośba będzie z city_centre do residential
                elif i in range(91, 121):
                    source = random.choice(self.addr.city_centre)
                    dest = random.choice(self.addr.residential)
                # z tego 10% szansy, że prośba będzie z residential do shops
                elif i in range(121, 141):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.shops)
                # z tego 10% szansy, że prośba będzie z shops do residential
                elif i in range(141, 161):
                    source = random.choice(self.addr.shops)
                    dest = random.choice(self.addr.residential)
                # z tego 10%(?) szansy, że będzie z jakiegokolwiek do jakiegokolwiek innego rejonu
                else:
                    source = random.choice(self.addr.all_addr)
                    dest = random.choice(self.addr.all_addr)
            elif datetime.strptime("10:00:00", "%H:%M:%S") < time < datetime.strptime(
                    "13:00:00", "%H:%M:%S"):
                print("middle of the day")
                # jest 5% szansy, że w każdej minucie w środku dnia wpłynie jakaś prośba
                if i in range(51, 1001):
                    return Request("_" + " " + "_", "_" + " " + "_", time, 0)
                # z tego 30% szansy, że prośba będzie z residential do city_centre
                elif i in range(1, 16):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.city_centre)
                # z tego 30% szansy, że prośba będzie z city_centre do residential
                elif i in range(16, 31):
                    source = random.choice(self.addr.city_centre)
                    dest = random.choice(self.addr.residential)
                # z tego 10% szansy, że prośba będzie z residential do shops
                elif i in range(31, 36):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.shops)
                # z tego 10% szansy, że prośba będzie shops do residential
                elif i in range(36, 41):
                    source = random.choice(self.addr.shops)
                    dest = random.choice(self.addr.residential)
                # z tego 20% szansy, że będzie z jakiegokolwiek do jakiegokolwiek innego rejonu
                else:
                    source = random.choice(self.addr.all_addr)
                    dest = random.choice(self.addr.all_addr)
            elif datetime.strptime("13:00:00", "%H:%M:%S") < time < datetime.strptime(
                        "18:00:00", "%H:%M:%S"):
                print("afternoon")
                # jest 20% szansy, że w każdej minucie po południu wpłynie jakaś prośba
                if i in range(201, 1001):
                    return Request("_" + " " + "_", "_" + " " + "_", time, 0)
                # z tego ok. 30% szansy, że prośba będzie ze schools do residential
                elif i in range(1, 61):
                    source = random.choice(self.addr.schools)
                    dest = random.choice(self.addr.residential)
                # z tego ok. 15% szansy, że prośba będzie z residential do city_centre
                elif i in range(61, 91):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.city_centre)
                # z tego ok. 15% szansy, że prośba będzie z city_centre do residential
                elif i in range(91, 121):
                    source = random.choice(self.addr.city_centre)
                    dest = random.choice(self.addr.residential)
                # z tego ok. 10% szansy, że prośba będzie z residential do shops
                elif i in range(121, 141):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.shops)
                # z tego ok. 10% szansy, że prośba będzie z shops do residential
                elif i in range(141, 161):
                    source = random.choice(self.addr.shops)
                    dest = random.choice(self.addr.residential)
                # z tego 10%(?) szansy, że będzie z jakiegokolwiek do jakiegokolwiek innego rejonu
                else:
                    source = random.choice(self.addr.all_addr)
                    dest = random.choice(self.addr.all_addr)
            elif datetime.strptime("18:00:00", "%H:%M:%S") < time < datetime.strptime(
                        "21:00:00", "%H:%M:%S"):
                print("evening")
                # jest 10% szansy, że w każdej minucie wieczorem wpłynie jakaś prośba
                if i in range(101, 1001):
                    return Request("_" + " " + "_", "_" + " " + "_", time, 0)
                # z tego ok. 30% szansy, że prośba będzie z residential do city_centre
                elif i in range(1, 31):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.city_centre)
                # z tego ok. 30% szansy, że prośba będzie z city_centre do residential
                elif i in range(31, 61):
                    source = random.choice(self.addr.city_centre)
                    dest = random.choice(self.addr.residential)
                # z tego ok. 15% szansy, że prośba będzie z residential do shops
                elif i in range(61, 76):
                    source = random.choice(self.addr.residential)
                    dest = random.choice(self.addr.shops)
                # z tego ok. 15% szansy, że prośba będzie z shops do residential
                elif i in range(76, 91):
                    source = random.choice(self.addr.shops)
                    dest = random.choice(self.addr.residential)
                # z tego 10%(?) szansy, że będzie z jakiegokolwiek do jakiegokolwiek innego rejonu
                else:
                    source = random.choice(self.addr.all_addr)
                    dest = random.choice(self.addr.all_addr)
            else:
                print("night")
                # jest 2% szansy, że w każdej minucie nocy wpłynie jakaś prośba
                if i in range(21, 1001):
                    return Request("_" + " " + "_", "_" + " " + "_", time, 0)
                # z tego 100% szansy, że będzie z jakiegokolwiek do jakiegokolwiek obszaru
                else:
                    source = random.choice(self.addr.all_addr)
                    dest = random.choice(self.addr.all_addr)
            # wyznaczam drogę i sprawdzam, czy nie jest za krótka; jeśli jest,
            # to prośba wyznaczana jest na nowo
            graph = ox.graph_from_place("Iłża, Poland", network_type='drive')  # pobieram graf Iłży z przejezdnymi ulicami
            nodes, edges = ox.graph_to_gdfs(graph)
            geocoded_place = ox.geocode_to_gdf(source[0] + " " + source[1] + ", Iłża", which_result=1)
            geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
            origin = geocoded_place["geometry"].centroid.values[0]
            geocoded_place = ox.geocode_to_gdf(dest[0] + " " + dest[1] + ", Iłża", which_result=1)
            geocoded_place = geocoded_place.to_crs(CRS(edges.crs))
            destination = geocoded_place["geometry"].centroid.values[0]
            if osmnx.distance.euclidean_dist_vec(origin.y, origin.x, destination.y, destination.x) < (0.5 / 83):
                print("Too close to each other!")
                print("Origin: " + source[0] + " " + source[1] + ", Iłża")
                print("Destination: " + dest[0] + " " + dest[1] + ", Iłża")
                print("Distance: ", osmnx.distance.euclidean_dist_vec(origin.y, origin.x, destination.y, destination.x))
            else:
                break

        return Request(source[0] + " " + source[1], dest[0] + " " + dest[1], time, 1 + i % 6)
