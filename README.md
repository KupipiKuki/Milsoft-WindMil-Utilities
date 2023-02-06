# Milsoft-WindMil-Utilities
Collection of python tools to read and edit milsoft windmil model and export for GIS

Currently Work in Progress  
1. eqdb_read.py  
   - Reads in data from .seq equipm,ent database and stores each type in a pandas dataframe.  
   - Similar to WindMil will allow mass changes to equipment prior to DSS analysis.  
2. model_read_gid.py
   - Reads the .std file and stores the results in a dataframe, converts to lat/lon.  
   - exports to a shape file for import into QGIS or similar.  
