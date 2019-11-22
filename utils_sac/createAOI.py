import geopandas as gpd
from shapely import wkt
from datetime import datetime
import pandas as pd

def create_lat_lon(aoi_wkt):
    aoi = gpd.GeoDataFrame(pd.DataFrame({'geoms':[wkt.loads(aoi_wkt)]}), geometry='geoms')
    area_json = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [
                    aoi.bounds.minx.values[0],
                    aoi.bounds.maxy.values[0]
                ],
                [
                    aoi.bounds.maxx.values[0],
                    aoi.bounds.maxy.values[0]
                ],
                [
                    aoi.bounds.maxx.values[0],
                    aoi.bounds.miny.values[0]
                ],
                [
                    aoi.bounds.minx.values[0],
                    aoi.bounds.miny.values[0]
                ],
                [
                    aoi.bounds.minx.values[0],
                    aoi.bounds.maxy.values[0]
                ]
              ]
            ]
          }
        }
      ]
    }

    lons, lats = zip(*area_json["features"][0]["geometry"]["coordinates"][0])
    lat_extents = (min(lats), max(lats))
    lon_extents = (min(lons), max(lons))
    return lat_extents, lon_extents
