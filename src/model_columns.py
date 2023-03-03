# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 12:36:12 2023

@author: jmc53
"""

#Descriptions must be less then 10 characters per Shape requirments

start_columns=['Name','Type','Phase','Parent','MapNum','X2','Y2']
skipA=[50,51,52]
skipB=[60,62]
end_columnsA=['A_Energized','B_Energized','C_Energized','X1','Y1',
             'RotAngle','CircuitLvl','UplineSrc','UplineFdr']
end_columnsB=['X1','Y1','CircuitLvl','UplineSrc','UplineFdr']
end_columns=['CircuitLvl','UplineSrc','UplineFdr']

circuit_level=dict({0:'Xmission',
                    1:'Primary',
                    2:'Secondary'})

skip_line=[7,28,29,30]+list(range(34,59))+skipB
line=['A_Cond','B_Cond','C_Cond','N_Cond','ZLength','Const','LoadMix',
      'LoadZone','LoadLoc','LoadGrowth','BillingRef','A_KW','B_KW',
      'C_KW','A_KVAR','B_KVAR','C_KVAR','A_Cons','B_Cons','C_Cons',
      'X1','Y1','NumNeut']

line_columns=start_columns+line+end_columns

skip_all=list(range(7,56))+[58]+skipB

all_columns=start_columns+end_columnsB

capacitor=['A_KVAR','B_KVAR','C_KVAR','VoltRating','SwitchType','SwitchStat',
           'OnSetting','OffSetting','CtlElement','Connection','Total_KVAR',
           'CtlPhase']

skip_cap=[7]+list(range(20,56))+[58]+skipB

cap_columns=start_columns+capacitor+end_columnsB

capacitor_type=dict({0:'ShuntWye',
                     1:'ShuntDelta',
                     2:'ShuntAsPar',
                     3:'Series'})

capacitor_status=dict({0:'Disconnect',
                       1:'On',
                       2:'Off'})

capacitor_switch=dict({0:'Manual',
                       1:'Voltage',
                       2:'Current',
                       3:'ReactiveA',
                       4:'Time',
                       5:'Temp'})

regulator=['RegType','CtrlPhase','Winding','A_Desc','B_Desc','C_Desc',
           'A_VoltOut','B_VoltOut','C_VoltOut','A_R_LDC','B_R_LDC',
           'C_R_LDC','A_X_LDC','B_X_LDC','C_X_LDC','A_1st_Hi',
           'B_1st_Hi','C_1st_Hi','A_1st_Lo','B_1st_Lo','C_1st_Lo',
           'A_Bypass','B_Bypass','C_Bypass','AllSame','CtlElement']

skip_reg=[7,29,30,31]+list(range(37,56))+[58]+skipB

reg_columns=start_columns+regulator+end_columnsB

transformer = ['Winding','PriTapV','PriRatedV','SecRatedV','OD_SrcConn',
               'TerRactedV','TerChild','NomSecV','NomTerV','A_KVA',
               'B_KVA','C_KVA','A_Desc','B_Desc','C_Desc','CenterTap',
               'Mounting']

skip_xfmr=[7,9,12,22,23]+list(range(29,56))+[58]+skipB

xfmr_columns=start_columns+transformer+end_columnsB

xfmr_dtype = {'A_KVA':'float64',
              'B_KVA':'float64',
              'C_KVA':'float64'}

opendelta=dict({4:'AB',
                5:'AC',
                6:'BC'})

switch = ['Status','ID','PartnerID']

skip_sw = [7]+list(range(11,56))+[58]+skipB

sw_columns=start_columns+switch+end_columnsB

node = ['FeederNum','LoadCtlPt','LoadMix','LoadZone','LoadLoc',
        'LoadGrowth','BillingRef','A_KW','B_KW','C_KW','A_KVAR',
        'B_KVAR','C_KVAR','A_Cons','B_Cons','C_Cons','Mandatory',
        'NodeCirLvl','LoadInType','A_Parent','B_Parent','C_Parent',
        'IsMultiPar','ConsType','FdrColor']

skip_node=[7]+list(range(33,56))+[58]+skipB

node_columns=start_columns+node+end_columnsB

zsm = ['MinDesc','MaxDesc','SubNum','BusVoltage','OH_Zg_MinF','UG_Zg_MinF',
       'NomVoltage','LoadCtlPt','WyeDelta','RegCode','FdrColor']

skip_zsm=[7,18,19,20,21]+list(range(23,56))+[58]+skipB

zsm_columns=start_columns+zsm+end_columnsB

device = ['A_Desc','B_Desc','C_Desc','A_Closed','B_Closed','C_Closed',
          'ClsAllPh','LoadCtlPt','IsFdrBay','FdrNum','FdrColor','FdrName']

skip_dev=[7]+list(range(20,56))+[58]+skipB

dev_columns=start_columns+device+end_columnsB

motor = ['Status','HorsePwr','Running_PF','PercentEff',
         'kV_Rated','DropOutLim','NemaType','StartLimit',
         'SoftStType','SoftSt_R','SoftSt_X','SoftStTap',
         'LkdRotPwr','LkdRotMult','AdvModel','AdvCondEq',
         'AdvInPwr','PerUtil']

generator = ['Model','HoldV_Real','HoldV_Imag','KW_Out','Mx_KW_out','Mx_KVAR_Ld',
             'Mx_KVAR_Lg','WyeDelta']

mot_gen=['SdyStCond','TrnsCond','SbTrnsCond','Rated_KV','LoadMix',
         'LoadZone','LoadLoc','LoadGrowth','A_KW','B_KW','C_KW',
         'A_KVAR','B_KVAR','C_KVAR','A_Cons','B_Cons','C_Cons']

skip_mot=[7]+[25,34,39,42,43]+list(range(48,56))+[58]+skipB

skip_gen=[7]+[28,33]+list(range(35,56))+[58]+skipB

mot_columns=start_columns+mot_gen+motor+end_columnsB

gen_columns=start_columns+mot_gen+generator+end_columnsB

consumers=['LoadMix','LoadZone','LoadGrowth','BillingRef','A_KW',
           'B_KW','C_KW','A_KVAR','B_KVAR','C_KVAR','A_Cons','B_Cons',
           'C_Cons','LoadInType','IsActive','ConsType','MeterNum']

skip_cons=[7]+list(range(25,56))+[58]+skipB

cons_columns=start_columns+consumers+end_columnsB

eq_types_to_wm={'overhead':1,
                'capacitor':2,
                'underground':3,
                'regulator':4,
                'transformer':5,
                'switch':6,
                'node':8,
                'source':9,
                'device':10,
                'motor':11,
                'generator':12,
                'consumer':13}

eq_types_from_wm={1:'overhead',
                  2:'capacitor',
                  3:'underground',
                  4:'regulator',
                  5:'transformer',
                  6:'switch',
                  8:'node',
                  9:'source',
                  10:'device',
                  11:'motor',
                  12:'generator',
                  13:'consumer'}

eq_format={'overhead':[skip_line,line_columns,dict()],
           'capacitor':[skip_cap,cap_columns,dict()],
           'underground':[skip_line,line_columns,dict()],
           'regulator':[skip_reg,reg_columns,dict()],
           'transformer':[skip_xfmr,xfmr_columns,xfmr_dtype],
           'switch':[skip_sw,sw_columns,dict()],
           'node':[skip_node,node_columns,dict()],
           'source':[skip_zsm,zsm_columns,dict()],
           'device':[skip_dev,dev_columns,dict()],
           'motor':[skip_mot,mot_columns,dict()],
           'generator':[skip_gen,gen_columns,dict()],
           'consumer':[skip_cons,cons_columns,dict()],
           'all':[skip_all,all_columns,dict()],
           'lines':[skip_line,line_columns,dict()]}