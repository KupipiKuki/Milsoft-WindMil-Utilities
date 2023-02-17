# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:16:53 2023

@author: jmc53
"""


import pandas as pd
import model_columns as mc
import gis_process_df as gisdf
import sqlite3 as sql

#sql_engine = create_engine('sqlite://', echo=False)

lines_combined=True
generate_lines_db=True
lines_db_type='sql' #csv or sql, default sql

equip_basic_combined=True
generate_equip_db=True
equip_db_type='sql' #csv or sql, default sql


#by_feeder=True

folder_path='gdf_test\\'

file_prefix=['Lines','OH','UG','All','Cap','Reg','Xfmr','Sw','Node','Zsm','Dev','Mot','Gen','Cons']
file_sep='_'
file_suffix='geo'
file_type='.shp'


print('Read Data')

test=pd.read_csv('Milsoft_Export.std',header=None,skiprows=[0],low_memory=False)
mpt=pd.read_csv('Milsoft_Export.mpt',header=None,skiprows=[0],low_memory=False)

#sub_names=test[61].value_counts()
#circuit_names=test[63].value_counts()


print('Process Line Data')
if lines_combined:
    pData=gisdf.process_df(test,[1,3],mpt.copy(),dataset=True)
    pData.sort(mc.skip_line,mc.line_columns)
    
    pData.sort_db()
    line_db=pData.get_data_db()
    if generate_lines_db:
        if lines_db_type == 'csv':
            for entry in line_db.keys():
                line_db[entry].to_csv(folder_path+'lines_db.csv')
        else:
            db_connect = sql.connect(folder_path+'lines.db')
            for entry in line_db.keys():
                line_db[entry].to_sql(entry, con=db_connect,if_exists='replace')
    
    pData.prep_line_points()
    pData.crs_adjust(line=True)
    pData.gen_lines()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[0]+file_sep+file_suffix+file_type)
else:
    pData=gisdf.process_df(test,1,mpt.copy())
    pData.sort(mc.skip_line,mc.line_columns)
    pData.prep_line_points()
    pData.crs_adjust(line=True)
    pData.gen_lines()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[1]+file_sep+file_suffix+file_type)
    pData=gisdf.process_df(test,3,mpt.copy())
    pData.sort(mc.skip_line,mc.line_columns)
    pData.prep_line_points()
    pData.crs_adjust(line=True)
    pData.gen_lines()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[2]+file_sep+file_suffix+file_type)
print('Lines done')

if equip_basic_combined:
    print('Process Equipment')
    pData=gisdf.process_df(test,[2,4,5,6,9,10,11,12,13],dataset=True)
    pData.sort(mc.skip_all,mc.all_columns)
    
    pData.sort_db()
    equip_db=pData.get_data_db()
    if generate_equip_db:
        if equip_db_type == 'csv':
            for entry in equip_db.keys():
                equip_db[entry].to_csv(folder_path+entry+'_db.csv')
        else:
            db_connect = sql.connect(folder_path+'equip.db')
            for entry in equip_db.keys():
                equip_db[entry].to_sql(entry, con=db_connect,if_exists='replace')
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[3]+file_sep+file_suffix+file_type)
    print('All Equipment Done')
else:
    print('Process Capacitors')
    pData=gisdf.process_df(test,2)
    pData.sort(mc.skip_cap,mc.cap_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[4]+file_sep+file_suffix+file_type)
    print('Capacitors Done')
    
    print('Process Regulators')
    pData=gisdf.process_df(test,4)
    pData.sort(mc.skip_reg,mc.reg_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[5]+file_sep+file_suffix+file_type)
    print('Regulators Done')
    
    print('Process Transformers')
    #Column data types must be adjsted
    dtype_adjust = {'A_KVA':'float64',
                    'B_KVA':'float64',
                    'C_KVA':'float64'}
    
    pData=gisdf.process_df(test,5)
    pData.sort(mc.skip_xfmr,mc.xfmr_columns,type_adjust=dtype_adjust)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[6]+file_sep+file_suffix+file_type)
    print('Transformers Done')
    
    print('Process Switch')
    pData=gisdf.process_df(test,6)
    pData.sort(mc.skip_sw,mc.sw_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[7]+file_sep+file_suffix+file_type)
    print('Switch Done')
    
    print('Process Node')
    pData=gisdf.process_df(test,8)
    pData.sort(mc.skip_node,mc.node_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[8]+file_sep+file_suffix+file_type)
    print('Node Done')
    
    print('Process Source')
    pData=gisdf.process_df(test,9)
    pData.sort(mc.skip_zsm,mc.zsm_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[9]+file_sep+file_suffix+file_type)
    print('Source Done')
    
    print('Process Device')
    pData=gisdf.process_df(test,10)
    pData.sort(mc.skip_dev,mc.dev_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[10]+file_sep+file_suffix+file_type)
    print('Device Done')
    
    print('Process Motor')
    pData=gisdf.process_df(test,11)
    pData.sort(mc.skip_mot,mc.mot_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[11]+file_sep+file_suffix+file_type)
    print('Motor Done')
    
    print('Process Generator')
    pData=gisdf.process_df(test,12)
    pData.sort(mc.skip_gen,mc.gen_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[12]+file_sep+file_suffix+file_type)
    print('Generator Done')
    
    print('Process Consumers')
    pData=gisdf.process_df(test,13)
    pData.sort(mc.skip_cons,mc.cons_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath=folder_path,filename=file_prefix[13]+file_sep+file_suffix+file_type)
    print('Consumers Done')