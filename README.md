# Milsoft-WindMil-Utilities
Collection of python tools to read and edit milsoft windmil model and export for GIS

Currently Work in Progress  
1. eqdb_read.py  
   - Reads in data from .seq equipm,ent database and stores each type in a pandas dataframe.  
   - Similar to WindMil will allow mass changes to equipment prior to DSS analysis. 
2. model_read_gis.py  
   - Reads the .std file and stores the results in a dataframe, converts to lat/lon.  
   - exports to a shape file for import into QGIS or similar.  
   - Modified to ustilize a loop function calling the new class structure.  
     -  Currently shape file and database file creation controlled by a dictionary.  
3. gis_process_df.py  
   - This is the class associated with model_read_gis.  
   - Contains mutliple functions to generate and manipulate the data.  
4. model_columns.py  
   - lists and dictionaries to configure columns to be named and columns to be dropped.  
5. kukitestfunctions.py  
   - Funcxtions designed for testing and error checking used accross multiple projects.