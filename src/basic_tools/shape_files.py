# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:12:03 2023

@author: jmc53
"""
import geopandas as gpd
from shapely.geometry import Point, Polygon
import pandas as pd

names=['cs03_fixed']

for n in names:
    df = pd.read_csv(n+'.csv')
    #df['Temp']=df[["X","Y"]].apply(list, axis=1)
    df['geometry'] = df.apply(lambda row: Point(row.X, row.Y), axis=1)
    df.drop(['X','Y'],axis=1,inplace=True)
    
    gdf  = gpd.GeoDataFrame(df,crs='EPSG:3517')
    
    gdf.to_file('.\shp\\'+n+'.shp')