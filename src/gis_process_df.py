# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:34:51 2023

@author: jmc53

"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np
from pyproj import Transformer
import model_columns as mc
import sqlite3 as sql
import kukitestfunctions as tfn

class process_df:
    """
    process_df\n
    \n
    input_df - required, pandas dataframe created from milsoft std file\n
    category - required, int or list of categories to be processed\n
    points_df - optional, pandas dataframe for vertices of element in input_df, milsoft mpt file\n
    dataset - optional, boolean, instructs to build database from unused columns\n
    append - optional, boolean, instructs to append all categories in the database, use with caution, if configured wrong can cause crash\n
    name - optional, string, will assign name to database entry for int or appended category\n
    Important Note, if a name is added ensure it is added to the eq_format dictionary in model_columns
    """
    def __init__(self,input_df,category,points_df=None,dataset=False,append=False,name=None,addname=False):
        if type(category) is int:
            self.data_df=input_df.loc[input_df[1]==category].copy()
        elif type(category) is list:
            self.data_df=input_df.loc[input_df[1].isin(category)].copy()
        else:
            raise TypeError("category must be an int or a list, invalid: {0}".format(type(category)))
        self.dataset=dataset
        self.data_db=None
        if self.dataset:
            self.data_db=dict()
            if type(category) is list:
                if not append:
                    for cat in category:
                        self.data_db[mc.eq_types_from_wm[cat]]=input_df.loc[input_df[1]==cat].copy()
                else:
                    if tfn.testIsNotEmptyString(name):
                        if name not in mc.eq_format.keys():
                            if addname:
                                mc.eq_format[name]=[mc.skip_all,mc.all_columns,dict()]
                            else:
                                print("{} not found in dictionary, please use addname=True to add it as a basic entry or modify the model_columns.py file to add a detailed entry".format(name))
                        self.data_db[name]=input_df.loc[input_df[1].isin(category)].copy()
                    else:
                        self.data_db[mc.eq_types_from_wm[category[0]]]=input_df.loc[input_df[1].isin(category)].copy()
            else:
                if tfn.testIsNotEmptyString(name):
                    self.data_db[name]=self.data_df.copy()
                else:
                    self.data_db[mc.eq_types_from_wm[category]]=self.data_df.copy()#Already did this
        self.pl_data=[]
        self.pl_df=points_df
    
    def gen_shape_database(self,drop_columns,columns,filepath='',filename=None,sqlname='sql_db',isLine=False,db_type='csv'):
        """
        gen_shape_database\n
        Generates the shape file and if initially set a database file
        \n
        drop_columns - required, list of columns to drop from the dataframe\n
        columns - required, list of column names for the remaining columns\n
        filepath - optional, folder location to ecport files, will store in project directory by default\n
        filename - optional, file name for the shape file\n
        salname - optional, file name for the sql database\n
        isLine - optional, Set True to create lines, False for points, default is false\n
        db_type - optional, set database type, 'csv' or 'sql', default is 'csv'
        """
        self.sort(drop_columns,columns)
        
        if self.data_db:
            self.sort_db()
            self.export_db(db_type,filepath,sqlname=sqlname)
        
        if isLine:
            self.prep_line_points()
            self.crs_adjust(line=True)
            self.gen_lines()
        else:
            self.crs_adjust()
            self.gen_points()
        
        self.export_geo_pd(filepath=filepath,filename=filename)

    def sort(self,drop_columns,columns,type_adjust=None):
        if len(drop_columns)>0:
            self.data_df.drop(axis=1,columns=drop_columns,inplace=True)
        self.data_df.columns=columns
        if type(type_adjust) is dict:
            self.data_df=self.data_df.astype(type_adjust)
    
    def sort_db(self):
        for key in self.data_db:
            if len(mc.eq_format[key][0])>0:
                self.data_db[key].drop(axis=1,columns=mc.eq_format[key][0],inplace=True)
            self.data_db[key].columns=mc.eq_format[key][1]
            if mc.eq_format[key][2]:
                self.data_db[key]=self.data_db[key].astype(mc.eq_format[key][2])
        
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
    
    def get_data_db(self):
        return self.data_db
    
    def export_db(self,db_type='csv',path='',sqlname='sql_db'):
        if db_type == 'csv':
            for entry in self.data_db.keys():
                self.data_db[entry].to_csv(path+entry+'.csv')
        else:
            db_connect = sql.connect(path+sqlname+'.db')
            for entry in self.data_db.keys():
                self.data_db[entry].to_sql(entry, con=db_connect,if_exists='replace')