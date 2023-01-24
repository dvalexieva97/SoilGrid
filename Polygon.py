
import pandas as pd
from Point import Point
import matplotlib.pyplot as plt
from shapely.geometry import Point as shp
import geopandas as gpd
from geopandas import GeoDataFrame
import logging
from utils import find_soil_type

class Polygon:
    """
    Class represeting a polygon made of points (tuples of coordinates)
    """
    def __init__(self, coordinates_list, data_parse_map):
        self.coordinates_list = coordinates_list
        self.points = []
        self.data_parse_map = data_parse_map
        self.df = pd.DataFrame()
        self.required_metadata = ["id", "latitude", "longitude", "soil_category"]

    def get_point_data(self, find_soil_type=True):

        for i, (lat, long) in enumerate(self.coordinates_list):
            point = Point(lat, long, self.data_parse_map)
            point.run()
            point.id = i
            self.points.append(point)
        if find_soil_type:
            self.add_soil_types()

    def points_to_dataframe(self):
        for point in self.points:
            dict_ = {k:v for k,v in point.__dict__.items() if k in self.required_metadata +
                     list(self.data_parse_map.keys())}
            df_point = pd.DataFrame(dict_, index=[point.id])
            self.df = pd.concat([self.df, df_point])


    def add_soil_types(self):
        for pt in self.points:
            pt.soil_category = find_soil_type(pt.soil_silt_content, pt.soil_sand_content, pt.soil_clay_content)

    def plot_values(self,
                    val_to_plot: str,
                    buffer_val: float = 0.2,
                    save_path: str = None,
                    to_save: bool = True,
                    world_datapath: str = 'naturalearth_lowres'):


        if not save_path:
            save_path = f"./output_data/{val_to_plot}.png"

        world = gpd.read_file(gpd.datasets.get_path(world_datapath))

        geometry = [shp(xy) for xy in zip(self.df['longitude'], self.df['latitude'])]
        gdf = GeoDataFrame(self.df, geometry=geometry)

        gdf_temp = gdf[["geometry", val_to_plot]]

        fig, ax = plt.subplots()
        world.plot(ax=ax, alpha=1, color='grey')
        gdf_temp.plot(ax=ax, marker='+', label=val_to_plot.replace("_", " ").title(), cmap="PRGn_r")
        ax.set_ylim(auto=True)

        # Add colour legend:
        plot = ax.pcolor(self.df[[val_to_plot]], cmap="PRGn_r")
        fig.colorbar(plot, cmap="PRGn_r")

        plt.legend(prop={'size': 15})
        # Add buffer to bounds for better visualization of our values
        temp_ = gdf.copy()
        temp_ = temp_.buffer(buffer_val)
        minx, miny, maxx, maxy = temp_.total_bounds
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)

        if to_save:
            plt.savefig(save_path)
            logging.info(f"Saved geoplot at {save_path}")
            plt.close()