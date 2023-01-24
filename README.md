# SoilGrid

SoilGrid is a Python library to extract and visualize soil data from coordinates.  

*Created by: Dianka Alexieva*

## Installation
First install the requirements.txt  

For MacOS: geopandas has trouble being set up on MacOS. In addition to the Python libraries neeed (see in requeremetns.txt), 
you need to set up gdal using brew to be able to install it.
This will enable you to install 'fiona' which gives access to global maps, as opposed to simply plotting a map with your
 own coordinates
```
brew install gdal
$ export PATH=/Library/Frameworks/GDAL.framework/Versions/2.2/Programs:$PATH
$ gdal-config --version
# Install same gdal version as your gdal-config:
$ pip install gdal==3.6.2
$ pip install fiona
``` 

## Usage

```python
from Polygon import Polygon
lat = "43.50157756165822"
long = "5.335927322474049"
data_map = {"soil_organic_matter": "ORCDRC_M_sl1_250m_ll_0-30cm.tif",}
polygon = Polygon([lat, long], data_map)
polygon.run()
# creates polygon object from a list of lat, long tuples
for k in data_map.keys():
   polygon.plot_values(val_to_plot=k)
```
**data_map** is a dictionary mapping between the attribute name of a Point and the key poiting to that attribute.
In the Point class we have a method which finds the values of the data key, no matter how nested it is in our input geojson

### General structure
General structure - we have two main classes: a Point, created with one coordinate (latitude and longitude),
and a Polygon, composed of a list of coordinates.
Working with classes allows for easy manipulation and extention of our objects.
the Point.run() method executes an API call to get soil attribute details and parses their values.  
To improve: create a soil attribute subclass and store additional information, such as the measurement unit, attribute 
description etc.

### Soil attributes of a Point
Any attributes can automatically be added to the Point object by simply adding additoinal dictoinary keys to the
data_map input of a Point / Polygon. 

### Plotting a Polygon with soil data
For each desired attribute we can print the polygon's data from its composing points.  
To improve: use a more meaningful basemap, as the polygon's scale is so small that the geopandas world map doesn't 
give any information (or if not zooming on based on our points, we can see the world but not our individual 
coordinates and their soil attribute values).

### Computing the Soil Type (Category)

For simplification, we assumed there are 4 soil categories, represented by the soil content percentange of each 
silt, clay and sand. An example mapping of a representatoin of the soil category triangle 
is present in utils.py (soil_triangle_map).  
The function determines the soil type per point simply compares the point's values to the triangle mapping.

### Saving data
Plotting differenet soil polygon atributes also saves them into the output_data dir, 
as well as the input geopandas df.

### Next steps
- Adding a feature to interpolate Polygon values and plot them.
- Add better basemaps
- Check out smarter approaches to compute the soil category from a soil type triangle
- Improve testing
- Library handling using poetry, .toml
- Move configurations to config.yml

