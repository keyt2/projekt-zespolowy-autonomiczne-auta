import numpy as np
import pandas as pd
from request import Request
import osmnx as ox
import random
from randomtimestamp import random_time


class RequestGenerator:
    buildings = pd.DataFrame(ox.geometries_from_place("Iłża, Poland", tags={'building': True}))
    addresses = np.column_stack((buildings.loc[ :, 'addr:street'], buildings.loc[ :, 'addr:housenumber']))
    addresses = np.array(addresses, dtype=str)
    addresses = addresses[~np.any(addresses == 'nan', axis=1)]

    def generate_request(self):
        source = random.choice(self.addresses)
        destination = random.choice(self.addresses)
        return Request(source[0] + " " + source[1], destination[0] + " " + destination[1], random_time())




rg = RequestGenerator()
r = rg.generate_request().show()