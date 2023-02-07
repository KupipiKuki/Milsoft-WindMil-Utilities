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
import model_columns as mc

class process_df:
    def __init__(self,input_df,category,points_df=None):
        if type(category) is int:
            self.data_df=input_df.loc[test[1]==category].copy()
        elif type(category) is list:
            self.data_df=input_df.loc[test[1].isin(category)].copy()
        else:
            raise TypeError("category must be an int or a list, invalid: {0}".format(type(category)))
        self.pl_data=[]
        self.pl_df=points_df

    def sort(self,drop_columns,columns,type_adjust=None):
        self.data_df.drop(axis=1,columns=drop_columns,inplace=True)
        self.data_df.columns=columns
        if type(type_adjust) is dict:
            self.data_df=self.data_df.astype(dtype_adjust)
        
    def crs_adjust(self,from_crs="epsg:3517",to_crs='EPSG:4326',line=False):
        crs_transform = Transformer.from_crs(from_crs,to_crs,always_xy=False)
        crs_transform.transform(self.data_df['X1'],self.data_df['Y1'],inplace=True)
        self.data_df['Coord1']=self.data_df[["Y1","X1"]].apply(list, axis=1)
        if line:
            crs_transform.transform(self.data_df['X2'],self.data_df['Y2'],inplace=True)
            self.data_df['Coord2']=self.data_df[["Y2","X2"]].apply(list, axis=1)
        if 'X2' in self.data_df.columns and 'Y2' in self.data_df.columns:
            self.data_df.drop(axis=1,columns=['X1','Y1','X2','Y2'],inplace=True)
        else:
            self.data_df.drop(axis=1,columns=['X1','Y1'],inplace=True)
        if self.pl_df is not None:
            crs_transform.transform(self.pl_df['X'],self.pl_df['Y'],inplace=True)
            self.pl_df['Coord']=self.pl_df[["Y","X"]].apply(list, axis=1)
            self.pl_df.drop(axis=1,columns=['X','Y'],inplace=True)
            
    def gen_points(self):
        if 'Coord1' in self.data_df.columns:
            for idx, row in self.data_df.iterrows():
                self.pl_data.append(Point(row['Coord1']))
            self.data_df.drop(axis=1,columns=['Coord1'],inplace=True)
        else:
            print('Error, missing columns, run sort then crs_adjust!')
    
    def gen_lines(self):
        mpt_groups=self.pl_df.groupby(['Name'])['Coord'].apply(lambda x: x.tolist())
        self.data_df['CoordMid']=self.data_df['Name'].map(mpt_groups)
        self.data_df['CoordMid']=self.data_df['CoordMid'].apply(lambda x: [] if type(x) is not list else x)
        self.data_df['CoordMid'].apply(lambda x: [] if np.isnan(x).all() else x)
        for idx, row in self.data_df.iterrows():
            temp=[row['Coord1']]+row['CoordMid']+[row['Coord2']]
            self.pl_data.append(LineString(temp))

        self.data_df.drop(axis=1,columns=['Coord1','CoordMid','Coord2'],inplace=True)
        
    def export_geo_pd(self,filepath='',filename='export_geo.shp',crs='EPSG:4326'):
        if len(self.pl_data)>0:
            geo_df = gpd.GeoDataFrame(self.data_df, geometry=self.pl_data, crs = crs)
            geo_df.to_file(filepath+filename)
        else:
            print('Error, no geometry found')
    
    def prep_line_points(self):
        if self.pl_df is not None:
            self.pl_df.drop(axis=1,columns=3,inplace=True)
            self.pl_df.columns = ['Name','X','Y']
        else:
            print('Error, no points found!')
    
    def head(self,rows=None):
        if type(rows) is int:
            return self.data_df.head(rows)
        else:
            return self.data_df.head()
            
    def get_df(self):
        return self.data_df

coord_transform = Transformer.from_crs( "epsg:3517","epsg:4326",always_xy=False)

print('Read Data')

test=pd.read_csv('Milsoft_Export.std',header=None,skiprows=[0],low_memory=False)
mpt=pd.read_csv('Milsoft_Export.mpt',header=None,skiprows=[0],low_memory=False)


print('Process Line Data')
# =============================================================================
# pData=process_df(test,[1,3],mpt.copy())
# pData.sort(mc.skip_line,mc.line_columns)
# pData.prep_line_points()
# pData.crs_adjust(line=True)
# pData.gen_lines()
# pData.export_geo_pd(filepath='lines_test\\',filename='Lines_geo.shp')
# print('test done')
# =============================================================================
pData=process_df(test,1,mpt.copy())
pData.sort(mc.skip_line,mc.line_columns)
pData.prep_line_points()
pData.crs_adjust(line=True)
pData.gen_lines()
pData.export_geo_pd(filepath='lines_test\\',filename='OH_geo.shp')
pData=process_df(test,3,mpt.copy())
pData.sort(mc.skip_line,mc.line_columns)
pData.prep_line_points()
pData.crs_adjust(line=True)
pData.gen_lines()
pData.export_geo_pd(filepath='lines_test\\',filename='UG_geo.shp')
print('Lines done')

print('Process Capacitors')
pData=process_df(test,2)
pData.sort(mc.skip_cap,mc.cap_columns)
pData.crs_adjust()
pData.gen_points()
pData.export_geo_pd(filepath='lines_test\\',filename='Cap_geo.shp')
print('Capacitors Done')

print('Process Regulators')
pData=process_df(test,4)
pData.sort(mc.skip_reg,mc.reg_columns)
pData.crs_adjust()
pData.gen_points()
pData.export_geo_pd(filepath='lines_test\\',filename='Reg_geo.shp')
print('Regulators Done')

print('Process Transformers')
#Column data types must be adjsted
dtype_adjust = {'A_KVA':'float64',
                'B_KVA':'float64',
                'C_KVA':'float64'}

pData=process_df(test,5)
pData.sort(mc.skip_xfmr,mc.xfmr_columns,type_adjust=dtype_adjust)
pData.crs_adjust()
pData.gen_points()
pData.export_geo_pd(filepath='lines_test\\',filename='Xfmr_geo.shp')
print('Transformers Done')
