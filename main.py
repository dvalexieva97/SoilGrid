from Polygon import Polygon
from utils import read_geojson

import logging
logging.basicConfig(level = logging.INFO)

if __name__ == "__main__":

    # 0. Variables:
    data_parse_map = {
        "soil_acidity": "PHIHOX_M_sl1_250m_ll_by10_0-30cm.tif",
                      "soil_organic_matter": "ORCDRC_M_sl1_250m_ll_0-30cm.tif",
                      "soil_water_capacity": "AWCh1_M_sl1_250m_ll_pF2.3_0-30cm.tif",
                      "soil_clay_content": "CLYPPT_M_sl1_250m_ll_0-30cm.tif",
                      "soil_sand_content": "SNDPPT_M_sl1_250m_ll_0-30cm.tif",
                      "soil_silt_content": "SLTPPT_M_sl1_250m_ll_0-30cm.tif",
                      }
    geodf_path = "./output_data/geodata.csv"

    # 1. Get coordinates from geojson:
    coordinates = read_geojson()

    # 2. Form polygon from coordinates:
    polygon = Polygon(coordinates, data_parse_map)

    # 3. Get data defined in dictoinary for each of our polygon points
    polygon.get_point_data()

    # 4. Dataframe from points objects inside Polygon:
    polygon.points_to_dataframe(find_soil_type=True)
    logging.info(f"Created geodataframe:\n{polygon.df.head()}")
    if geodf_path:
        polygon.df.to_csv(geodf_path)

    # 5. Plot values
    for k in data_parse_map.keys():
        polygon.plot_values(val_to_plot=k)

