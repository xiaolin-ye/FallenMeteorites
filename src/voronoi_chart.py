# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 09:28:41 2022

@author: xy
"""

import geopandas as gpd
import pandas as pd

import matplotlib.pyplot as plt
from shapely.ops import unary_union
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords

df = pd.read_csv(r'.\data\meteorite-landings.csv')
fallen_meteors = df[df['fall'] == 'Fell'].dropna()
#fallen_meteors = fallen_meteors[fallen_meteors['year']>1950]

geometry = gpd.points_from_xy(fallen_meteors.reclong, fallen_meteors.reclat)
geodata = gpd.GeoDataFrame(fallen_meteors, geometry=geometry)
geodata.crs = "EPSG:4326"
world = gpd.read_file(r'.\data\ne_50m_admin_0_countries.shp')

# fig, ax = plt.subplots(figsize=(12, 10))
# world.plot(ax=ax, color='gray')
# geodata.plot(ax=ax, markersize=3.5, color='black')
# ax.axis('off')
# plt.axis('equal')
# plt.show()

world = world.to_crs(epsg=4326)
geodata_proj = geodata.to_crs(world.crs)

world_shape = unary_union(world.geometry)

contain =[]
for x in geodata_proj.geometry:
    contain.append(world_shape.contains(x))

geodata_proj = geodata_proj[contain]
coords = points_to_coords(geodata_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, world_shape)

#%%
fig, ax = subplot_for_map(figsize=(100,100))
plot_voronoi_polys_with_points_in_area(ax, world_shape, region_polys, coords, region_pts)
ax.set_title('Historical Fallen Meteorites',fontsize=100)
plt.tight_layout()
plt.savefig(r'.\fig\Historical Fallen Meteorites.png',bbox_inches='tight')
plt.show()
