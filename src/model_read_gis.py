# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 13:16:53 2023

@author: jmc53
"""


import pandas as pd
import model_columns as mc
import gis_process_df as gisdf

lines_combined=True
equip_basic_combined=True

print('Read Data')

test=pd.read_csv('Milsoft_Export.std',header=None,skiprows=[0],low_memory=False)
mpt=pd.read_csv('Milsoft_Export.mpt',header=None,skiprows=[0],low_memory=False)

sub_names=test[61].value_counts()
circuit_names=test[63].value_counts()


print('Process Line Data')
if lines_combined:
    pData=gisdf.process_df(test,[1,3],mpt.copy())
    pData.sort(mc.skip_line,mc.line_columns)
    pData.prep_line_points()
    pData.crs_adjust(line=True)
    pData.gen_lines()
    pData.export_geo_pd(filepath='lines_test\\',filename='Lines_geo.shp')
else:
    pData=gisdf.process_df(test,1,mpt.copy())
    pData.sort(mc.skip_line,mc.line_columns)
    pData.prep_line_points()
    pData.crs_adjust(line=True)
    pData.gen_lines()
    pData.export_geo_pd(filepath='lines_test\\',filename='OH_geo.shp')
    pData=gisdf.process_df(test,3,mpt.copy())
    pData.sort(mc.skip_line,mc.line_columns)
    pData.prep_line_points()
    pData.crs_adjust(line=True)
    pData.gen_lines()
    pData.export_geo_pd(filepath='lines_test\\',filename='UG_geo.shp')
print('Lines done')

if equip_basic_combined:
    print('Process Equipment')
    pData=gisdf.process_df(test,[2,4,5,6,9,10,11,12,13])
    pData.sort(mc.skip_all,mc.all_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='All_geo.shp')
    print('All Equipment Done')
else:
    print('Process Capacitors')
    pData=gisdf.process_df(test,2)
    pData.sort(mc.skip_cap,mc.cap_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Cap_geo.shp')
    print('Capacitors Done')
    
    print('Process Regulators')
    pData=gisdf.process_df(test,4)
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
    
    pData=gisdf.process_df(test,5)
    pData.sort(mc.skip_xfmr,mc.xfmr_columns,type_adjust=dtype_adjust)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Xfmr_geo.shp')
    print('Transformers Done')
    
    print('Process Switch')
    pData=gisdf.process_df(test,6)
    pData.sort(mc.skip_sw,mc.sw_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Sw_geo.shp')
    print('Switch Done')
    
    print('Process Node')
    pData=gisdf.process_df(test,8)
    pData.sort(mc.skip_node,mc.node_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Node_geo.shp')
    print('Node Done')
    
    print('Process Source')
    pData=gisdf.process_df(test,9)
    pData.sort(mc.skip_zsm,mc.zsm_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Zsm_geo.shp')
    print('Source Done')
    
    print('Process Device')
    pData=gisdf.process_df(test,10)
    pData.sort(mc.skip_dev,mc.dev_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Dev_geo.shp')
    print('Device Done')
    
    print('Process Motor')
    pData=gisdf.process_df(test,11)
    pData.sort(mc.skip_mot,mc.mot_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Mot_geo.shp')
    print('Motor Done')
    
    print('Process Generator')
    pData=gisdf.process_df(test,12)
    pData.sort(mc.skip_gen,mc.gen_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Gen_geo.shp')
    print('Generator Done')
    
    print('Process Consumers')
    pData=gisdf.process_df(test,13)
    pData.sort(mc.skip_cons,mc.cons_columns)
    pData.crs_adjust()
    pData.gen_points()
    pData.export_geo_pd(filepath='lines_test\\',filename='Cons_geo.shp')
    print('Consumers Done')