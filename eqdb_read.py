# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 09:06:14 2023

@author: jmc53
"""

import pandas as pd

test=pd.read_csv('Milsoft_Export.seq',header=None,skiprows=[0])

ovLen=10
overhead=['Name','Type','Material','Capacity','Res25Deg','Res50Deg',
          'GMR','PreferedNeut','Diameter','Category']
ugLen=19
underground=['Name','Type','TypeUG','Capacity','ResPhase','GMR',
             'ResNeut','StrandsNeut','InsOD','CableOD','Diaelectric',
             'DiameterUnderNeut','NeutGMR','DiameterConductor',
             'DistanceCN']
underground_type=dict({0:'Concentric',
                       1:'Tape Shield',
                       2:'No Concentric'})
zsmLen=21
zsm=['Name','Type','Capacity','UnitType','BaseKVA','BaseKV','Unit',
     'Self_R','Self_jX','Self_jB','Mutual_R','Mutual_jX','Mutual_jB',
     'Pos_R','Pos_jX','Zero_R','Zero_jX','Mutual_Rev_R','Mutual_Rev_jX',
     'Neg_R','Neg_jX']

zabcLen=25
zabc=['Name','Type','Capacity','UnitType','BaseKVA','BaseKV','Unit',
      'AA_R','AA_jX','AB_R','AB_jX','AC_R','AC_jX',
      'BA_R','BA_jX','BB_R','BB_jX','BC_R','BC_jX',
      'CA_R','CA_jX','CB_R','CB_jX','CC_R','CC_jX']

xfmrLen=28
xfmrDrop=[23]+list(range(xfmrLen,len(test.columns)))
xfmr=['Name','Type','Ampacity','CondType','Percent_Z_PriSec',
      'Percent_Z_PriTer','Percent_Z_SecTer','XR_PriSec','XR_PriTer','XR_SecTer',
      'BaseKVA_PriSec','BaseKVA_PriTer','BaseKVA_SecTer','Ground_R_Pri',
      'Ground_R_Sec','Ground_R','Ground_X_Pri','Ground_X_Sec','Ground_X',
      'K_Factor','No_Load_Loss_PriSec','No_Load_Loss_PriTer',
      'No_Load_Loss_SecTer','RatedKVA_PriSec','RatedKVA_PriTer',
      'RatedKVA_SecTer','Padmount']

regLen=8
regDrop=list(range(regLen,len(test.columns)))
reg=['Name','Type','Ampacity','CTR','Per_Boost','Per_Buck','Step_Size','Bandwidth']

loadLen=6
loadDrop=list(range(loadLen,len(test.columns)))
load=['Name','Type','KVA','Z','Current','Connection']

constLen=29
constDrop=[27]+list(range(constLen,len(test.columns)))
const=['Name','Type','1P_GMDP','2P_GMDP','3P_GMDP','1P_GMDPN','2P_GMDPN',
       '3P_GMDPN','UG_GMDP','Height_Ground','Height_Unit','OD_Distance',
       'Distance_Unit','Spacing','Max_Volts','Transposition',
       '1P_Pos','2P_Pos','3P_Pos',
       'A_Vert_Pos','B_Vert_Pos','C_Vert_Pos','N_Vert_Pos',
       'A_Horz_Pos','B_Horz_Pos','C_Horz_Pos','N_Horz_Pos',
       'UG_GMDPN']

zoneLen=3
zoneDrop=list(range(zoneLen,len(test.columns)))
zone=['Name','Type','Growth_Rate',]

devLen=21
devDrop=[16]+list(range(devLen,len(test.columns)))
dev=['Name','Type','Group','Current_Rating','Max_Sym_Fault',
     'Max_Asym_Fault','Ground_Pickup','Volts_Nom','Fast_Trip_Phase',
     'Slow_Trip_Phase','Hydraulic','LightTable','LT_Control',
     'LT_Operate','Not_Ganged','Phase_Pickup','Phase_Enabled',
     'Ground_Enabled','Fast_Trip_Ground','Slow_Trip_Ground']

pdevLen=9
pdevDrop=list(range(pdevLen,len(test.columns)))
pdev=['Name','Type','Desc','Coord_Pt1','Coord_Pt2','Protected_KV','Device_KV','Multiplier','Fault_Type']

amsLen=6
asmDrop=list(range(amsLen,len(test.columns)))
asm=['Name','Type','Category','Asm_Type','Element_Type','Desc']

swgLen=49
swgDrop=list(range(swgLen,len(test.columns)))
swg=['Name','Type','SwitchGearType','CabinetCount',
     'Cab1_Number','Cab1_Type','Cab1_A_Name','Cab1_B_Name','Cab1_C_Name',
     'Cab2_Number','Cab2_Type','Cab2_A_Name','Cab2_B_Name','Cab2_C_Name',
     'Cab3_Number','Cab3_Type','Cab3_A_Name','Cab3_B_Name','Cab3_C_Name',
     'Cab4_Number','Cab4_Type','Cab4_A_Name','Cab4_B_Name','Cab4_C_Name',
     'Cab5_Number','Cab5_Type','Cab5_A_Name','Cab5_B_Name','Cab5_C_Name',
     'Cab6_Number','Cab6_Type','Cab6_A_Name','Cab6_B_Name','Cab6_C_Name',
     'Cab7_Number','Cab7_Type','Cab7_A_Name','Cab7_B_Name','Cab7_C_Name',
     'Cab8_Number','Cab8_Type','Cab8_A_Name','Cab8_B_Name','Cab8_C_Name',
     'Cab9_Number','Cab9_Type','Cab9_A_Name','Cab9_B_Name','Cab9_C_Name',]

eqdb=dict({'OH':None,
           'UG':None,
           'ZSM':None,
           'ZABC':None,
           'XFMR':None,
           'VREG':None,
           'LOAD':None,
           'CONST':None,
           'ZONE':None,
           'DEV':None,
           'PDEV':None,
           'ASM':None,
           'SWGEAR':None})

#for index, row in test.iterrows():
#    if row[1] == 1:
#        print(row[0:ovLen])

overhead_df=test.loc[test[1]==1].copy()
overhead_df.drop(axis=1,columns=list(range(ovLen,len(test.columns))),inplace=True)
overhead_df.columns=overhead

underground_df=test.loc[test[1]==2].copy()
underground_df.drop(axis=1,columns=[10,13,14,15]+list(range(ugLen,len(test.columns))),inplace=True)
underground_df.columns=underground

zsm_df=test.loc[test[1]==3].copy()
zsm_df.drop(axis=1,columns=list(range(zsmLen,len(test.columns))),inplace=True)
zsm_df.columns=zsm

zabc_df=test.loc[test[1]==4].copy()
zabc_df.drop(axis=1,columns=list(range(zabcLen,len(test.columns))),inplace=True)
zabc_df.columns=zabc

xfmr_df=test.loc[test[1]==5].copy()
xfmr_df.drop(axis=1,columns=xfmrDrop,inplace=True)
xfmr_df.columns=xfmr

reg_df=test.loc[test[1]==6].copy()
reg_df.drop(axis=1,columns=regDrop,inplace=True)
reg_df.columns=reg

load_df=test.loc[test[1]==7].copy()
load_df.drop(axis=1,columns=loadDrop,inplace=True)
load_df.columns=load

const_df=test.loc[test[1]==8].copy()
const_df.drop(axis=1,columns=constDrop,inplace=True)
const_df.columns=const

zone_df=test.loc[test[1]==9].copy()
zone_df.drop(axis=1,columns=zoneDrop,inplace=True)
zone_df.columns=zone

dev_df=test.loc[test[1]==10].copy()
dev_df.drop(axis=1,columns=devDrop,inplace=True)
dev_df.columns=dev

pdev_df=test.loc[test[1]==11].copy()
pdev_df.drop(axis=1,columns=pdevDrop,inplace=True)
pdev_df.columns=pdev

asm_df=test.loc[test[1]==12].copy()
asm_df.drop(axis=1,columns=asmDrop,inplace=True)
asm_df.columns=asm

swg_df=test.loc[test[1]==12].copy()
swg_df.drop(axis=1,columns=swgDrop,inplace=True)
swg_df.columns=swg