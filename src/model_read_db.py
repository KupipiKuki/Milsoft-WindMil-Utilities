# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:16:53 2023

@author: jmc53
"""


import pandas as pd
import model_columns as mc
import gis_process_df as gisdf

folder_path=''#'gdf_test\\'

file_sep='_'
file_suffix='geo'
file_type='.shp'

#name,column(s),isLine,append,mpt,generatedb,dbtype
file_prefix_wm={0:['lines',[1,3],True,True,True,True,'sql'],
                1:['overhead',1,True,False,True,True,'csv'],
                2:['capacitor',2,False,False,False,True,'csv'],
                3:['underground',3,True,False,True,True,'csv'],
                4:['regulator',4,False,False,False,True,'csv'],
                5:['transformer',5,False,False,False,True,'csv'],
                6:['switch',6,False,False,False,True,'csv'],
                8:['node',8,False,False,False,True,'csv'],
                9:['source',9,False,False,False,True,'csv'],
                10:['device',10,False,False,False,True,'csv'],
                11:['motor',11,False,False,False,True,'csv'],
                12:['generator',12,False,False,False,True,'csv'],
                13:['consumer',13,False,False,False,True,'csv'],
                51:['transformer',5,False,False,False,False,'csv'],#NISC
                52:['transformer',5,False,False,False,False,'csv'],#Milsoft
                99:['all',[2,4,5,6,9,10,11,12,13],False,False,False,True,'sql']}

type_col={0:['lines',[1,3]],
          99:['all',[2,4,5,6,9,10,11,12,13]]}


print('Read Data')

test=pd.read_csv('Milsoft_Export.std',header=None,skiprows=[0],low_memory=False)
#mpt=None
mpt=pd.read_csv('Milsoft_Export.mpt',header=None,skiprows=[0],low_memory=False)

process_cat=[0,1,2,3,4,5,6,9,10,11,12,13]

for proc in process_cat:
    print('Process {} Data'.format(file_prefix_wm[proc][0]))
    if file_prefix_wm[proc][5]:
        if file_prefix_wm[proc][4]:
            pData=gisdf.process_df(test,file_prefix_wm[proc][1],mpt.copy(),dataset=True,append=file_prefix_wm[proc][3],name=file_prefix_wm[proc][0])
        else:
            pData=gisdf.process_df(test,file_prefix_wm[proc][1],dataset=True,append=file_prefix_wm[proc][3],name=file_prefix_wm[proc][0])
        
    else:
        if file_prefix_wm[proc][4]:
            pData=gisdf.process_df(test,file_prefix_wm[proc][1],mpt.copy())
        else:
            pData=gisdf.process_df(test,file_prefix_wm[proc][1])
        
        if proc==51:
            pData.sort([7,9,12,22,23]+list(range(29,51)),
                       mc.start_columns+mc.transformer)
        else:
            pData.sort([7,9,12,22,23]+list(range(29,64)),
                       mc.start_columns+mc.transformer)
        l1=pData.get_df()
        l=l1.set_index('Name')
        l.to_csv(folder_path+file_prefix_wm[proc][0]+'.csv')
    print('{} Done'.format(file_prefix_wm[proc][0]))
