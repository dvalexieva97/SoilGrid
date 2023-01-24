
import json
import logging

defaultpath_ = "./input_data/test.geojson"
soil_triangle_map = {
    "Sandy clay":
        {"clay": range(0, 50),
         "silt": range(0, 20),
         "sand": range(50, 100)},
    "Silty clay":
        {"clay": range(50, 100),
         "silt": range(50, 100),
         "sand": range(0, 50)},
    "Loam":
        {"clay": range(50, 100),
         "silt": range(20, 50),
         "sand": range(0, 50)},
    "Silt Loam":
        {"clay": range(0, 50),
         "silt": range(20, 50),
         "sand": range(50, 100)},

}

def read_geojson(path_=None, defaultpath=defaultpath_):
    """
    :param path_: path to geojson file
    :return: list of tuples of coordinates forming a polygon
    """

    if not path_:
        path_ = defaultpath

    with open(path_, "r") as f:
        geo_dict = json.load(f)

    features = geo_dict["features"]
    if len(features) == 1:
        features = features[0]
        if not ("geometry" in str(features) and "coordinates" in str(geo_dict)):
            raise Exception("Unexpected geodictionary structure!")
        if features["geometry"]["type"] != "Polygon":
            raise Exception(f"Wrong geo object type! Expecting Polygon, you have input {features['type']}")
        else:
            return [tuple(x) for x in features["geometry"]["coordinates"][0]]
            # todo check why it is a list of list of lists and not list of list
    else:
        raise Exception("Multiple feature items in your Polygon, do not know how to handle!")



def find_soil_type(silt_content, sand_content, clay_content,
                   soil_triangle_map=soil_triangle_map):

    for k, dict_ in soil_triangle_map.items():

        if silt_content in dict_["silt"]:
            if sand_content in dict_["sand"]:
                if clay_content in dict_["clay"]:
                    return k

    logging.warning(
        f"No soil category matching input values of (silt, sand, clay){silt_content, sand_content, clay_content}")
    return None
