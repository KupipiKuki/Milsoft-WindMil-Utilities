# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:16:53 2023

@author: jmc53
"""

from pyproj import Transformer
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import fiona
import numpy as np

coord_transform = Transformer.from_crs( "epsg:3517","epsg:4326",always_xy=False)

print('Read Data')

test=pd.read_csv('Milsoft_Export.std',header=None,skiprows=[0],low_memory=False)
mpt=pd.read_csv('Milsoft_Export.mpt',header=None,skiprows=[0],low_memory=False)

print('Process Data')

mpt.drop(axis=1,columns=3,inplace=True)
mpt.columns = ['Name','X','Y']

start_columns=['Name','Type','Phase','Parent','MapNum','X2','Y2']
skipA=[50,51,52]
skipB=[60,62]
end_columns=['A_Energized','B_Energized','C_Energized','X1','Y1',
             'RotAngle','CircuitLvl','UplineSrc','UplineFdr']
end_columnsA=['UplineSrc','UplineFdr']

skip_oh=[7,28,29,30]+list(range(34,60))+skipB
overhead=['A_Cond','B_Cond','C_Cond','N_Cond','ZLength','Const','LoadMix',
          'LoadZone','LoadLoc','LoadGrowth','BillingRef','A_KW','B_KW',
          'C_KW','A_KVAR','B_KVAR','C_KVAR','A_Cons','B_Cons','C_Cons',
          'X1','Y1','NumNeut']

overhead_df=test.loc[test[1]==1].copy()
overhead_df.drop(axis=1,columns=skip_oh,inplace=True)
overhead_df.columns=start_columns+overhead+end_columnsA
coord_transform.transform(overhead_df['X1'],overhead_df['Y1'],inplace=True)
coord_transform.transform(overhead_df['X2'],overhead_df['Y2'],inplace=True)
overhead_df['Coord1']=overhead_df[["Y1","X1"]].apply(list, axis=1)
overhead_df['Coord2']=overhead_df[["Y2","X2"]].apply(list, axis=1)
overhead_df.drop(axis=1,columns=['X1','Y1','X2','Y2'],inplace=True)

underground_df=test.loc[test[1]==3].copy()
underground_df.drop(axis=1,columns=skip_oh,inplace=True)
underground_df.columns=start_columns+overhead+end_columnsA
coord_transform.transform(underground_df['X1'],underground_df['Y1'],inplace=True)
coord_transform.transform(underground_df['X2'],underground_df['Y2'],inplace=True)
underground_df['Coord1']=underground_df[["Y1","X1"]].apply(list, axis=1)
underground_df['Coord2']=underground_df[["Y2","X2"]].apply(list, axis=1)
underground_df.drop(axis=1,columns=['X1','Y1','X2','Y2'],inplace=True)


coord_transform.transform(mpt['X'],mpt['Y'],inplace=True)
mpt['Coord']=mpt[["Y","X"]].apply(list, axis=1)
mpt.drop(axis=1,columns=['X','Y'],inplace=True)
mpt_groups=mpt.groupby(['Name'])['Coord'].apply(lambda x: x.tolist())

overhead_df['CoordMid']=overhead_df['Name'].map(mpt_groups)
overhead_df['CoordMid']=overhead_df['CoordMid'].apply(lambda x: [] if type(x) is not list else x)
overhead_df['CoordMid'].apply(lambda x: [] if np.isnan(x).all() else x)

underground_df['CoordMid']=underground_df['Name'].map(mpt_groups)
underground_df['CoordMid']=underground_df['CoordMid'].apply(lambda x: [] if type(x) is not list else x)
underground_df['CoordMid'].apply(lambda x: [] if np.isnan(x).all() else x)

line_strings=[]
print('Process OH Line Strings')
for idx, row in overhead_df.iterrows():
    temp=[row['Coord1']]+row['CoordMid']+[row['Coord2']]
    line_strings.append(LineString(temp))

overhead_df.drop(axis=1,columns=['Coord1','CoordMid','Coord2'],inplace=True)

geo_df = gpd.GeoDataFrame(overhead_df, geometry=line_strings, crs = 'EPSG:4326')

geo_df.to_file('lines\\OH_geo.shp')
    
line_strings=[]
print('Process UG Line Strings')
for idx, row in underground_df.iterrows():
    temp=[row['Coord1']]+row['CoordMid']+[row['Coord2']]
    line_strings.append(LineString(temp))

underground_df.drop(axis=1,columns=['Coord1','CoordMid','Coord2'],inplace=True)

geo_df = gpd.GeoDataFrame(underground_df, geometry=line_strings, crs = 'EPSG:4326')

geo_df.to_file('lines\\UG_geo.shp') 