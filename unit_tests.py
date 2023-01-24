from Point import Point
from Polygon import Polygon

data_parse_map = {"soil_acidity": "PHIHOX_M_sl1_250m_ll_by10_0-30cm.tif"}
long = "5.335927322474049"
lat = "43.50157756165822"

# todo import pytest

def test_point():
    point = Point(lat, long, data_parse_map)
    point.run()
    assert point.soil_acidity == 7.3

def test_polygon():
    polygon = Polygon([(lat, long)], data_parse_map)
    polygon.get_point_data(find_soil_type=False)
    for pt in polygon.points:
        assert pt.soil_acidity == 7.3
