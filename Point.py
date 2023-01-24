import pandas as pd
import requests
import logging
logging.basicConfig(level = logging.INFO)

class Point:

    def __init__(self, latitude, longitude, parse_map):
        self.latitude = latitude
        self.longitude = longitude
        self.geojson = {}
        self.verify_input()
        self.parse_map = parse_map

    def verify_input(self):
        if isinstance(self.latitude, str):
            self.latitude = float(self.latitude)
        if isinstance(self.longitude, str):
            self.longitude = float(self.longitude)

        assert -90 <= self.latitude <= 90
        assert -180 <= self.longitude <= 180

    def run(self):
        self.api_call()
        if self.geojson:
            self.parse_geojson()
        else:
            logging.critical("Geojson fetched unsuccessfully")

    def api_call(self, base_url:str = "https://isqaper.isric.org/isqaper-rest/api/1.0/query"):
        """
        :param base_url: Base  API url
        :return: dict object with returned value from json
        """

        query = {'lat': self.latitude, 'lon': self.longitude}
        r = requests.get(base_url, params=query)
        if r.status_code != 200:
            logging.critical(f"Unsuccessful response for {query}. Response: {r.text}")
            return None
        geojson = r.json()
        if isinstance(geojson, dict):
            self.geojson = geojson

    def findkeys(self, node, kv):
        if isinstance(node, list):
            for i in node:
                for x in self.findkeys(i, kv):
                    yield x
        elif isinstance(node, dict):
            if kv in node:
                yield node[kv]
            for j in node.values():
                for x in self.findkeys(j, kv):
                    yield x

    def parse_geojson(self, key_val:str="value"):
        logging.info(f"Searching for values for point ({self.latitude, self.longitude})")
        for attribute_, keyword in self.parse_map.items():
            res = list(self.findkeys(self.geojson.copy(), kv=keyword))
            res = set([x[key_val] for x in res])
            if len(res) == 1:
                res = list(res)[0]
                setattr(self, attribute_, res)
                logging.info(f"Successfully set value of {attribute_}")
            else:
                logging.critical(f"Inconsistency in data list of Point[{self.latitude, self.longitude}] "
                                 f"for attribute '{attribute_}', searched with keyword '{keyword}' "
                                 f"Values: {res} ")

# long = "5.335927322474049"
# lat = "43.50157756165822"
#
#
# point = Point(lat, long, data_parse_map)
# point.run()
# # point.api_call()
# # point.parse_geojson()
# point.soil_acidity
# point.soil_organic_matter
# point.soil_water_capacity
# point.soil_clay_content
# point.soil_sand_content
# point.soil_silt_content
# # todo unit test polygon:
