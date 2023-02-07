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

opendelta=dict({4:'AB',
                5:'AC',
                6:'BC'})