#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2022-07-30 14:53:41
 $ @LastEditTime : 2022-09-25 19:42:17
 $ @LastEditors  : Luma
 $ @Description  :    

 $ @FilePath     : \working\script\Python\reg_map\reg_map.py
'''
import os
import re
import sys
import logging
import argparse
import glob

import zipfile
import lxml

import pandas as pd
import numpy as np
from datetime import datetime as dt

class book:
    def __init__(self,file_name=None,sheet_name=None,author=None,name_rule=0,tar_file_name=''):
        self.book              = pd.read_excel(file_name,sheet_name=None if sheet_name is None else sheet_name,header=None)
        self.write_list        = []
        self.creat_info_dict   = {}
        self.tar_file_name_lst = []
        print(f"Start parsing {file_name}...")

        def get_excel_author(excel_file):
            zf = zipfile.ZipFile(excel_file)
            doc = lxml.etree.fromstring(zf.read('docProps/core.xml'))
            attr_nodes = doc.getchildren()
            return {'Author':attr_nodes[0].text,'Date':str(pd.to_datetime(attr_nodes[2].text).tz_convert(None)),'LastEditTime':str(pd.to_datetime(attr_nodes[3].text).tz_convert(None)),'LastEditors':attr_nodes[1].text}

        self.creat_info_dict = get_excel_author(file_name) if author is None else {'Author':author,'Date':{str(dt.now().replace(microsecond=0))},'LastEditTime':{str(dt.now().replace(microsecond=0))},'LastEditors':author}

        if sheet_name is None:
            for sheet_name,sheet_df in self.book.items():
                if (sheet_df.empty):
                    print(f'{sheet_name} is empty!')
                else:
                    tar_file_name_sheet = sheet_name+("_APB_CFG" if sheet_name.isupper() else "_apb_cfg")+'.sv' if ( tar_file_name == '' ) else tar_file_name
                    self.tar_file_name_lst.append(tar_file_name_sheet)
                    sheet(creat_info_dict=self.creat_info_dict,sheet_name=sheet_name,sheet_df=sheet_df,name_rule=name_rule,tar_file_name=tar_file_name_sheet)
        else:
            tar_file_name_sheet = sheet_name+("_APB_CFG" if sheet_name.isupper() else "_apb_cfg")+'.sv' if ( tar_file_name == '' ) else tar_file_name
            self.tar_file_name_lst.append(tar_file_name_sheet)
            sheet(creat_info_dict=self.creat_info_dict,sheet_name=sheet_name,sheet_df=self.book,name_rule=name_rule,tar_file_name=tar_file_name_sheet)

class sheet:
    tab = '    '

    def __init__(self,creat_info_dict=None,sheet_name=None,sheet_df=None,name_rule=0,tar_file_name=''):
        self.file_header = f'''
/*
* @Author       : {creat_info_dict['Author']}
* @Date         : {creat_info_dict['Date']}
* @LastEditTime : {creat_info_dict['LastEditTime']}
* @LastEditors  : {creat_info_dict['Author']}
* @Description  : {sheet_name} apb cfg
* @FilePath     : {os.path.abspath('.')}\{tar_file_name}
*/
'''
        self.name_rule         = 0

        self.port_lst          = []
        self.param_lst         = []
        self.wire_lst          = []
        self.control_lst       = []
        self.block_lst         = []
        self.rd_reg_lst        = []

        self.max_len_of_RegName     = 0
        self.max_len_of_FieldName   = 0
        self.max_len_of_port_name   = 0
        self.max_len_of_Name        = 0
        self.max_len_of_Width       = 0
        self.max_len_of_BaseAddr    = 0
        self.max_len_of_OffsetAddr  = 0
        self.max_len_of_group_name_suffix_wr_done    = 0
        self.max_len_of_extend_port_direction        = 0
        self.max_len_of_port_width  = 0
        self.max_len_of_wire_declare_left_val        = 0
        self.max_len_of_wire_declare_right_val       = 0

        self.clr_suffix        = ''
        self.clr_val_suffix    = ''
        self.set_suffix        = ''
        self.set_val_suffix    = ''
        self.tgl_suffix        = ''
        self.tgl_val_suffix    = ''
        self.max_len_of_name_suffix = 0

        self.rd_en_suffix      = ''
        self.wr_en_suffix      = ''

        self.entire_en_any     = 0
        self.shadow_en         = 0
        self.out_flag_en       = 0

        print(f"Start parsing {sheet_name}...")

        df = self.pre_process(sheet_df,name_rule)
        self.entire_en         = ( df.drop(df[df["FieldName"].str.lower() == "reserved"].index).RegAccess == df.drop(df[df["FieldName"].str.lower() == "reserved"].index).FiledAccess ).all()
        self.signal_update_en  = ( 'update_en' if self.name_rule else 'UpDateEn' ) if self.shadow_en else ""
        self.signal_rstn      = 'rst_n'     if self.name_rule else 'Rstn'
        self.signal_clk       = 'clk'       if self.name_rule else 'Clk'
        self.signal_p_sel     = 'p_sel'     if self.name_rule else 'PSel'
        self.signal_p_enbale  = 'p_enbale'  if self.name_rule else 'PEnable'
        self.signal_p_addr    = 'p_addr'    if self.name_rule else 'PAddr'
        self.signal_p_write   = 'p_write'   if self.name_rule else 'PWrite'
        self.signal_p_wr_data = 'p_wr_data' if self.name_rule else 'PWrData'
        self.signal_p_rd_data = 'p_rd_data' if self.name_rule else 'PRdData'

        self.cal_max_len(df)
        self.gen_module_head(sheet_name)

        for key,group in df.groupby(['Base\nAddress',"Offset\nAddress","RegName"],as_index=False,sort=False):
            group = self.group_check_and_cal(key,group)
            self.process_Reg(group=group,BaseAddress=key[0],OffsetAddress=key[1],RegName=key[2])

        self.gen_block_rd()

        self.gen_file(sheet_name,tar_file_name)

    def calc_reset_val(self,ResetValue=None,Len=None,FiledName=None,group_entire_en=0):
        rst_val_obj = re.match(r'\d*\'?([bohd]?)(\d+)',str(ResetValue).lower())
        if rst_val_obj is not None:
            ResetValue =''
            if rst_val_obj.group(1) == 'o':
                int_val    = int(rst_val_obj.group(2),base=8)
                ResetValue = f'{bin(int_val)[2:]:0>{Len}}' if group_entire_en else f"{Len}'h{hex(int_val)[2:]}"
            elif rst_val_obj.group(1) == 'b':
                int_val    = int(rst_val_obj.group(2),base=2)
                ResetValue = f'{bin(int_val)[2:]:0>{Len}}' if group_entire_en else f"{Len}'h{hex(int_val)[2:]}"
            elif rst_val_obj.group(1) == 'h':
                int_val    = int(rst_val_obj.group(2),base=16)
                ResetValue = f'{bin(int_val)[2:]:0>{Len}}' if group_entire_en else f"{Len}'h{hex(int_val)[2:]}"
            else:
                int_val    = int(rst_val_obj.group(2),base=10)
                ResetValue = f'{bin(int_val)[2:]:0>{Len}}' if group_entire_en else f"{Len}'h{hex(int_val)[2:]}"

            # if( int_val > int(hex(int('1'*Len,base=2)),16) ):
            #     logging.error(f'waring:@FiledName={FiledName},the value of ResetValue is out of range!')

            return int_val,ResetValue
        else:
            logging.error(f'waring:@FiledName={FiledName},the format of ResetValue is error!')

    def pre_process(self,df=None,name_rule=0):
        df.loc[0:1]=df.loc[0:1].fillna(method='ffill')
        df.columns = df.loc[1]
        df=df.drop([0,1])
        df.loc[:,["Base\nAddress","Offset\nAddress","RegName","Width","RegAccess"]]=df.loc[:,["Base\nAddress","Offset\nAddress","RegName","Width","RegAccess"]].fillna(method='ffill')
        df.loc[:,["RegAccess","FiledAccess"]]=df.loc[:,["RegAccess","FiledAccess"]].fillna(method='ffill',axis=1)
        df.loc[:,["Min"]]=df.loc[:,["Min"]].fillna(0)

        df["Shadow"]     = df["Shadow"].fillna(0)
        self.shadow_en   =  df.drop(df[df["FieldName"].str.lower() == "reserved"].index).Shadow.astype(str).str.lower().str.contains(r'1[rw]{0,2}',regex=True).any()
        self.out_flag_en =  df.drop(df[df["FieldName"].str.lower() == "reserved"].index).Shadow.astype(str).str.lower().str.contains(r'[rw]{0,2}',regex=True).any()

        if name_rule == 0:
            self.name_rule = df["FieldName"].str.contains('_').any()
        else:
            self.name_rule = name_rule - 1

        df.insert(7,"Len_Cal",df["Len"])
        df.insert(11,"FieldName_Cal",df["FieldName"].str.lower() if self.name_rule else df["FieldName"] )
        df.insert(16,"ResetValue_Cal",df["ResetValue"])

        for row_index in df.index:
            if pd.isnull(df.loc[row_index,"High"]):
                df.loc[row_index,"High"] = df.loc[row_index,"Low"]
            if pd.isnull(df.loc[row_index,"Low"]):
                df.loc[row_index,"Low"] = df.loc[row_index,"High"]
            df.loc[row_index,"Len_Cal"] = (df.loc[row_index,"High"] - df.loc[row_index,"Low"]) + 1

            if pd.isnull(df.loc[row_index,"Max"]):
                df.loc[row_index,"Max"] = int('1'*df.loc[row_index,"Len_Cal"],base=2)

            if( df.loc[row_index,"Len"] != df.loc[row_index,"Len_Cal"] ):
                logging.warning(f'waring:@FiledName={df.loc[row_index,"FieldName"]} in {df.loc[row_index,"RegName"]},Len is {df.loc[row_index,"Len"]},but {df.loc[row_index,"Len_Cal"]} is expected. ')

            rst_val_int,df.loc[row_index,"ResetValue_Cal"] = self.calc_reset_val(df.loc[row_index,"ResetValue"],df.loc[row_index,"Len"],df.loc[row_index,"FieldName"],0)

            if( rst_val_int < df.loc[row_index,"Min"] or rst_val_int > int(df.loc[row_index,"Max"]) ):
                logging.error(f'@FiledName={df.loc[row_index,"FieldName"]} in {df.loc[row_index,"RegName"]},the value of ResetValue is out of range!. ')


        return df

    def cal_max_len(self,df=None):
        wr_reg_add_suffix_en = 0
        for key,group in df.groupby(['Base\nAddress',"Offset\nAddress","RegName"],as_index=False,sort=False):
            group_entire_en = ( group.drop(group[group["FieldName"].str.lower() == "reserved"].index).RegAccess == group.drop(group[group["FieldName"].str.lower() == "reserved"].index).FiledAccess ).all()
            group_control_dict = {'wr_en':0,'wr_once':0,'wr_clear':0,'wr_set':0,'wr_one_clear':0,'wr_one_set':0,'wr_one_toggle':0,'wr_zero_clear':0,'wr_zero_set':0,'wr_zero_toggle':0,'rd_en':0,'rd_en_wr':0,'rd_only':0,'rd_clear':0,'rd_set':0}
            if( group_entire_en ):
                self.entire_en_any = 1
                group_control_dict = self.parse_Access(group["RegAccess"].unique()[0],key[2])
            if ( group_entire_en and group_control_dict['wr_en'] and group_control_dict['rd_en'] ):
                wr_reg_add_suffix_en = 1

        done_en            = 0
        suffix_en          = 0
        rd_en_reg          = 0
        wr_en_reg          = 0
        done_fieldname_lst = []
        for row_index in df.index:
            if( not( df.loc[row_index,"FieldName"].lower() == "reserved" ) ):
                control_dict = self.parse_Access(df.loc[row_index,"FiledAccess"],df.loc[row_index,"FieldName"])

            if ( control_dict['rd_en'] ):
                rd_en_reg = 1
            if ( control_dict['wr_en'] ):
                wr_en_reg = 1
            if ( control_dict['wr_once'] ):
                done_en = 1
                done_fieldname_lst.append(df.loc[row_index,"FieldName"])
            if ( control_dict['rd_clear'] or control_dict['rd_set'] or control_dict['rd_en_wr'] ):
                 suffix_en = 1
                 wr_en_reg = 1

        max_len_of_fixed_signal     = max(len(self.signal_rstn),len(self.signal_clk),len(self.signal_update_en),len(self.signal_p_sel),len(self.signal_p_enbale),len(self.signal_p_addr),len(self.signal_p_write),len(self.signal_p_wr_data),len(self.signal_p_rd_data))

        self.max_len_of_RegName     = max([len(str( reg_name )) for reg_name in df.RegName])
        self.max_len_of_FieldName   = max([len(str( filed_name )) for filed_name in df.FieldName])
        self.max_len_of_Name        = max([len(str( reg_name )) for reg_name in pd.concat([df.RegName,df.FieldName])])
        self.max_len_of_Width       = max([len(str( width )) for width in df.Width])
        self.max_len_of_BaseAddr    = max([len(str( hex(int(str(BaseAddress)[2:],base=16))[2:] )) for BaseAddress in df['Base\nAddress']])
        self.max_len_of_OffsetAddr  = max([len(str( hex(int(str(OffsetAddr)[2:],base=16))[2:] )) for OffsetAddr in df['Offset\nAddress']])

        self.max_len_of_port_width  = self.max_len_of_Width + len(' '+'['+'-1:'+']') #'[21-1:0]'
        self.max_len_of_port_name   = max(self.max_len_of_FieldName,max_len_of_fixed_signal)

        if( suffix_en ):
            self.clr_suffix     = '_clr'     if self.name_rule else 'Clr'
            self.clr_val_suffix = '_clr_val' if self.name_rule else 'ClrVal'
            self.set_suffix     = '_set'     if self.name_rule else 'Set'
            self.set_val_suffix = '_set_val' if self.name_rule else 'SetVal'
            self.tgl_suffix     = '_tgl'     if self.name_rule else 'Tgl'
            self.tgl_val_suffix = '_tgl_val' if self.name_rule else 'TglVal'

        if( self.shadow_en ):
            self.shadow_suffix  = '_shadow'

        if( self.out_flag_en ):
            self.rd_en_suffix   = '_rd_en' if self.name_rule else 'RdEn'
            self.wr_en_suffix   = '_wr_en' if self.name_rule else 'WrEn'

        self.max_len_of_name_suffix               = max(len(self.clr_val_suffix),len(self.set_val_suffix),len(self.tgl_val_suffix),len(self.rd_en_suffix),len(self.wr_en_suffix))

        max_len_of_done_fieldname                 = (self.max_len_of_RegName if self.entire_en else max([len(str( filed_name )) for filed_name in done_fieldname_lst]) ) if done_en else 0
        self.max_len_of_group_name_suffix_wr_done = max((self.max_len_of_RegName if self.entire_en else self.max_len_of_FieldName )+(len(self.shadow_suffix) if self.shadow_en else 0),max_len_of_done_fieldname + len('_wr_done')) if done_en else ((self.max_len_of_RegName if self.entire_en else self.max_len_of_FieldName )+(len(self.shadow_suffix) if self.shadow_en else 0))
        self.max_len_of_extend_port_direction     = 6 + (4 if wr_en_reg else 0) #'output reg'

        if ( rd_en_reg or wr_en_reg ):
            self.max_len_of_wire_declare_right_val = max(11+len(self.signal_p_sel)+len(self.signal_p_write)+len(self.signal_p_enbale),18+len(self.signal_p_addr)+self.max_len_of_RegName)# wire spi_wr_data_rd = ( PAddr == SPI_WR_DATA ) && apb_rd;
        self.max_len_of_wire_declare_left_val      = max(self.max_len_of_group_name_suffix_wr_done,(self.max_len_of_RegName + (len('_reg') if wr_reg_add_suffix_en else len('_wr'))))

    def gen_module_head(self,sheet_name=None):
        self.port_lst.append(f'''module {sheet_name}{"_APB_CFG" if sheet_name.isupper() else "_apb_cfg"}''')
        self.port_lst.append(f'''(''')
        self.port_lst.append(f'''{sheet.tab}//System''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+"         ":<{self.max_len_of_port_width}} {self.signal_rstn:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+"         ":<{self.max_len_of_port_width}} {self.signal_clk:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        if self.shadow_en:
            self.port_lst.append(f'''\n{sheet.tab}//Shadow update''')
            self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+"         ":<{self.max_len_of_port_width}} {self.signal_update_en:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''\n{sheet.tab}//APB''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+"         ":<{self.max_len_of_port_width}} {self.signal_p_sel:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+"         ":<{self.max_len_of_port_width}} {self.signal_p_enbale:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+" [32-1:0]":<{self.max_len_of_port_width}} {self.signal_p_addr:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+"         ":<{self.max_len_of_port_width}} {self.signal_p_write:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''{sheet.tab}{f'{"input":<{self.max_len_of_extend_port_direction}}'+" [32-1:0]":<{self.max_len_of_port_width}} {self.signal_p_wr_data:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
        self.port_lst.append(f'''{sheet.tab}{f'{"output reg":<{self.max_len_of_extend_port_direction}}'+" [32-1:0]":<{self.max_len_of_port_width}} {self.signal_p_rd_data:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')

        self.param_lst.append(f'\n//----------------------------local parameter---------------------------------------------')
        self.wire_lst.append(f'\n//----------------------------local wire/reg declaration------------------------------------------')
        self.control_lst.append(f'\n//----------------------------control logic---------------------------------------------')
        self.control_lst.append(f'''{"wire":<4} {'apb_wr':<{self.max_len_of_RegName+3}} = {self.signal_p_sel+' && '+self.signal_p_write+' && '+self.signal_p_enbale:<{self.max_len_of_wire_declare_right_val}};''')
        self.control_lst.append(f'''{"wire":<4} {'apb_rd':<{self.max_len_of_RegName+3}} = {self.signal_p_sel+' && '+'~'+self.signal_p_write+' && '+'~'+self.signal_p_enbale:<{self.max_len_of_wire_declare_right_val}};''')
        self.block_lst.append(f'\n//--------------------------------processing------------------------------------------------')

    def group_check_and_cal(self,key=None,group=None):
        if( group['Len_Cal'].sum() > group["Width"].mean() ):
                logging.warning(f'waring:@ {key} ,total Len is {group["Len_Cal"].sum()},but {group["Width"].mean()} is expected. ')

        group = group.reset_index(drop=True)

        low_last  = group["Width"].unique()[0]
        row_index = 0
        run_en    =1
        while run_en:
            if( ( group.loc[row_index,"High"] ) < ( low_last - 1 )):
                columns = group.columns
                group = pd.DataFrame(np.insert(group.values,row_index,values=[group.loc[row_index,"Base\nAddress"],group.loc[row_index,"Offset\nAddress"],group.loc[row_index,"RegName"],group.loc[row_index,"Width"],( low_last - 1 ),( group.loc[row_index,"High"] + 1 ),(( low_last - 1 ) - ( group.loc[row_index,"High"] + 1 ) + 1 ),(( low_last - 1 ) - ( group.loc[row_index,"High"] + 1 ) + 1 ),0,0,"reserved","reserved",group.loc[row_index,"RegAccess"],"RO",0,0,f"{(( low_last - 1 ) - ( group.loc[row_index,'High'] + 1 ) + 1 )}'h0",''],axis=0))
                group.columns = columns

            low_last  = group.loc[row_index,"Low"]
            row_index = row_index + 1
            run_en    = row_index <= group.index[-1]

        logging.debug(f'{key}\n{group}')
        return group

    def gen_block_rd(self):
        block_rd_lst = []
        for reg in self.rd_reg_lst:
            block_rd_lst.append(f'''{sheet.tab*2}{reg.upper()}:''')
            block_rd_lst.append(f'''{sheet.tab*3}{self.signal_p_rd_data} <= {reg.lower()};''')
        if( block_rd_lst ):
            self.block_lst.append(f'\n//APB read')
            self.block_lst.append(f'always @ ( * )')
            self.block_lst.append(f'begin')

            self.block_lst.append(f'''{sheet.tab}case( {self.signal_p_addr} )''')
            self.block_lst.extend(block_rd_lst)
            self.block_lst.append(f'''{sheet.tab*2}default:''')
            self.block_lst.append(f'''{sheet.tab*3}{self.signal_p_rd_data} <= 'h0;''')
            self.block_lst.append(f'{sheet.tab}endcase')
            self.block_lst.append(f'end\n')

    def parse_Access(self,Access=None,FiledName=None):
        access_lst = ['RW','RO','WRC','WRS','WO','W1','WO1','RC','RS','WC','WS','WCRS','WSRC','W0C','W0S','W1C','W1S','W0T','W1T','W0SRC','W0CRS','W1SRC','W1CRS','WOC','WOS']
        wr_en_lst          = ['RW','WRC','WRS','WO','W1','WO1']
        wr_once_lst        = ['W1','WO1']
        wr_clear_lst       = ['WC','WCRS','WOC']
        wr_set_lst         = ['WS','WSRC','WOS']
        wr_one_clear_lst   = ['W1C','W1CRS']
        wr_one_set_lst     = ['W1S','W1SRC']
        wr_one_toggle_lst  = ['W1T']
        wr_zero_clear_lst  = ['W0C','W0CRS']
        wr_zero_set_lst    = ['W0S','W0SRC']
        wr_zero_toggle_lst = ['W0T']
        rd_en_lst          = ['RW','RO','WRC','WRS','W1','RC','RS','WC','WS','WCRS','WSRC','W0C','W0S','W1C','W1S','W0T','W1T','W0SRC','W0CRS','W1SRC','W1CRS']
        rd_en_wr_lst       = wr_clear_lst + wr_set_lst + wr_one_clear_lst + wr_one_set_lst + wr_one_toggle_lst + wr_zero_clear_lst + wr_zero_set_lst + wr_zero_toggle_lst
        rd_only_lst        = ['RO']
        rd_clear_lst       = ['RC','WRC','WSRC','W0SRC','W1SRC']
        rd_set_lst         = ['RS','WRS','WCRS','W0CRS','W1CRS']

        control_dict = {'wr_en':0,'wr_once':0,'wr_clear':0,'wr_set':0,'wr_one_clear':0,'wr_one_set':0,'wr_one_toggle':0,'wr_zero_clear':0,'wr_zero_set':0,'wr_zero_toggle':0,'rd_en':0,'rd_en_wr':0,'rd_only':0,'rd_clear':0,'rd_set':0}
        if( Access.upper() in access_lst ):
            control_dict['wr_en']          = 1 if( Access.upper() in wr_en_lst          ) else 0
            control_dict['wr_once']        = 1 if( Access.upper() in wr_once_lst        ) else 0
            control_dict['wr_clear']       = 1 if( Access.upper() in wr_clear_lst       ) else 0
            control_dict['wr_set']         = 1 if( Access.upper() in wr_set_lst         ) else 0
            control_dict['wr_one_clear']   = 1 if( Access.upper() in wr_one_clear_lst   ) else 0
            control_dict['wr_one_set']     = 1 if( Access.upper() in wr_one_set_lst     ) else 0
            control_dict['wr_one_toggle']  = 1 if( Access.upper() in wr_one_toggle_lst  ) else 0
            control_dict['wr_zero_clear']  = 1 if( Access.upper() in wr_zero_clear_lst  ) else 0
            control_dict['wr_zero_set']    = 1 if( Access.upper() in wr_zero_set_lst    ) else 0
            control_dict['wr_zero_toggle'] = 1 if( Access.upper() in wr_zero_toggle_lst ) else 0
            control_dict['rd_en']          = 1 if( Access.upper() in rd_en_lst          ) else 0
            control_dict['rd_en_wr']       = 1 if( Access.upper() in rd_en_wr_lst       ) else 0
            control_dict['rd_only']        = 1 if( Access.upper() in rd_only_lst        ) else 0
            control_dict['rd_clear']       = 1 if( Access.upper() in rd_clear_lst       ) else 0
            control_dict['rd_set']         = 1 if( Access.upper() in rd_set_lst         ) else 0

            return control_dict
        else:
            logging.error(f'waring:@FiledName={FiledName},Access is illegal!')

    def process_Reg(self,group=None,BaseAddress=None,OffsetAddress=None,RegName=None):
        group_entire_en     = ( group.drop(group[group["FieldName"].str.lower() == "reserved"].index).RegAccess == group.drop(group[group["FieldName"].str.lower() == "reserved"].index).FiledAccess ).all()
        logging.debug(f'BaseAddress:{BaseAddress},OffsetAddress:{OffsetAddress},RegName:{RegName},group_entire_en={group_entire_en}')
        group_shadow_en     = group.drop(group[group["FieldName"].str.lower() == "reserved"].index).Shadow.astype(str).str.lower().str.contains(r'1[rw]{0,2}',regex=True).all()
        group_shadow_en_any = group.drop(group[group["FieldName"].str.lower() == "reserved"].index).Shadow.astype(str).str.lower().str.contains(r'1[rw]{0,2}',regex=True).any()
        logging.debug(f'BaseAddress:{BaseAddress},OffsetAddress:{OffsetAddress},RegName:{RegName},group_shadow_en={group_shadow_en},group_shadow_en_any={group_shadow_en_any}')

        # group_rst_val
        if( group_entire_en ):
            rst_val_list = []
            for row_index in group.index:
                rst_val_list.append(self.calc_reset_val(group.loc[row_index,"ResetValue"],group.loc[row_index,"Len_Cal"],group.loc[row_index,"FieldName"],group_entire_en)[1])
                group_rst_val = f"'h{hex(int(''.join(rst_val_list),2))[2:]}"

        # group_control
        group_out_flag_en =  group.drop(group[group["FieldName"].str.lower() == "reserved"].index).Shadow.astype(str).str.lower().str.contains(r'r',regex=True).any()

        group_control_dict = {'wr_en':0,'wr_once':0,'wr_clear':0,'wr_set':0,'wr_one_clear':0,'wr_one_set':0,'wr_one_toggle':0,'wr_zero_clear':0,'wr_zero_set':0,'wr_zero_toggle':0,'rd_en':0,'rd_en_wr':0,'rd_only':0,'rd_clear':0,'rd_set':0}
        w1_cst_en_reg    = 0
        suffix_en        = 0
        group_rd_ctrl_en = 0
        if( group_entire_en ):
            group_control_dict = self.parse_Access(group.loc[0,"RegAccess"],group.loc[0,"RegName"])
            w1_cst_en_reg      = group_control_dict['wr_one_clear'] or group_control_dict['wr_zero_clear'] or group_control_dict['wr_one_set'] or group_control_dict['wr_zero_set'] or group_control_dict['wr_one_toggle'] or group_control_dict['wr_zero_toggle']
            suffix_en          = group_control_dict['rd_clear'] or group_control_dict['rd_set'] or group_control_dict['rd_en_wr']
            if ( group_control_dict['rd_clear'] or group_control_dict['rd_set'] or ( group_control_dict['rd_only'] and group_out_flag_en ) ):
                group_rd_ctrl_en = 1
        else:
            for row_index in group.index:
                control_dict_for_flag = self.parse_Access(group.loc[row_index,"FiledAccess"],group.loc[row_index,"FieldName"])

                if ( control_dict_for_flag['wr_en'] ):
                    group_control_dict['wr_en'] = 1
                    if ( control_dict_for_flag['wr_once'] ):
                        group_control_dict['wr_once'] = 1
                if ( control_dict_for_flag['rd_en'] and not( group.loc[row_index,"FieldName"].lower() == "reserved" ) ):
                    group_control_dict['rd_en'] = 1
                if ( control_dict_for_flag['rd_clear'] or control_dict_for_flag['rd_set'] or ( control_dict_for_flag['rd_only'] and group_out_flag_en ) ):
                    group_rd_ctrl_en = 1
                if ( control_dict_for_flag['wr_one_clear'] or control_dict_for_flag['wr_zero_clear'] or control_dict_for_flag['wr_one_set'] or control_dict_for_flag['wr_zero_set'] or control_dict_for_flag['wr_one_toggle'] or control_dict_for_flag['wr_zero_toggle'] ):
                    w1_cst_en_reg = 1
                if ( control_dict_for_flag['rd_clear'] or control_dict_for_flag['rd_set'] or control_dict_for_flag['rd_en_wr'] ):
                     suffix_en = 1
                if ( control_dict_for_flag['rd_en_wr'] ):
                     group_control_dict['rd_en_wr'] = 1
        wr_reg_name = RegName.lower() + ('_reg' if ( group_entire_en and group_control_dict['wr_en'] and group_control_dict['rd_en'] ) else '')

        # group max_len
        group_rd_fieldname_lst = []
        group_wr_fieldname_lst = []
        for row_index in  group.drop(group[group["FieldName"].str.lower() == "reserved"].index).index:
            control_dict_for_max_len = self.parse_Access(group.loc[row_index,"FiledAccess"],group.loc[row_index,"FieldName"])
            if ( control_dict_for_max_len['rd_en'] ):
                group_rd_fieldname_lst.append(group.loc[row_index,"FieldName"])
            if ( control_dict_for_max_len['wr_en'] ):
                group_wr_fieldname_lst.append(group.loc[row_index,"FieldName"])

        max_len_of_group_rd_fieldname_lst = max([len(str( name )) for name in group_rd_fieldname_lst]) if group_rd_fieldname_lst else 0
        max_len_of_group_wr_fieldname_lst = max([len(str( name )) for name in group_wr_fieldname_lst]) if group_wr_fieldname_lst else 0
        max_len_of_group_name             =  max([len(str( name )) for name in group.FieldName])

        if group_entire_en:
            if( group_control_dict['wr_en'] and group_control_dict['rd_en'] ):
                max_len_of_group_left_name =  max([len(str( name )) for name in pd.concat([group.RegName,group.FieldName])])
            elif( group_control_dict['wr_en'] ):
                max_len_of_group_left_name =  max_len_of_group_wr_fieldname_lst
            else:
                max_len_of_group_left_name =  max([len(str( name )) for name in group.FieldName]) if suffix_en else len(str( wr_reg_name ))
        else:
            max_len_of_group_left_name = max([len(str( name )) for name in group.FieldName])

        if group_entire_en:
            if( group_control_dict['wr_en'] and group_control_dict['rd_en'] ):
                max_len_of_block_assign_right_val = max(max((max(len(str( wr_reg_name )),len(str(RegName)) + (len(self.shadow_suffix) if group_shadow_en_any else 0)) + (2*self.max_len_of_Width + 3)),max_len_of_group_rd_fieldname_lst),(max_len_of_group_name + ( (2*self.max_len_of_Width + 7 + len(self.signal_p_wr_data) if w1_cst_en_reg else 0 ))))#W1C/S/T #' & ~PWrData[13:11]'
            elif( group_control_dict['wr_en'] ):
                max_len_of_block_assign_right_val = max(max((max(len(str( wr_reg_name )),len(str( wr_reg_name )) + (len(self.shadow_suffix) if group_shadow_en_any else 0)) + (2*self.max_len_of_Width + 3))),(max_len_of_group_name + ( (2*self.max_len_of_Width + 7 + len(self.signal_p_wr_data))) if w1_cst_en_reg else 0 ))#W1C/S/T #' & ~PWrData[13:11]'
            else:
                max_len_of_block_assign_right_val = max(max_len_of_group_rd_fieldname_lst,(max_len_of_group_name + ( (2*self.max_len_of_Width + 7 + len(self.signal_p_wr_data)) if w1_cst_en_reg else 0 )))#W1C/S/T #' & ~PWrData[13:11]'
        else:
            max_len_of_block_assign_right_val = max_len_of_group_name + ( (2*self.max_len_of_Width + 7 + len(self.signal_p_wr_data)) if w1_cst_en_reg else 0 )  #W1C/S/T #' & ~PWrData[13:11]'

        max_len_of_block_assign_left_val  = max_len_of_group_left_name + self.max_len_of_name_suffix + 2*self.max_len_of_Width + 3 #[21:10]

        # group append
        # comment
        self.port_lst.append(f'\n{sheet.tab}//{RegName}')
        self.block_lst.append(f'\n//{RegName}')
        self.param_lst.append(f"localparam {RegName.upper():<{self.max_len_of_RegName}} = 32'h{hex(int(str(BaseAddress)[2:],base=16))[2:]:<{self.max_len_of_BaseAddr}} + 32'h{hex(int(str(OffsetAddress)[2:],base=16))[2:]:<{self.max_len_of_OffsetAddr}};")

        if ( group_control_dict['wr_once'] or group_control_dict['rd_en'] ):
            self.wire_lst.append(f'\n//{RegName}')
            if ( group_entire_en and group_control_dict['rd_en'] and group_control_dict['wr_en'] ):
                self.wire_lst.append(f'''{"reg":<4} [{group.Width.unique()[0]}-1:0] {wr_reg_name:<{self.max_len_of_wire_declare_left_val}};//wr''')
            self.wire_lst.append(f'''{"wire":<4} [{group.Width.unique()[0]}-1:0] {RegName.lower():<{self.max_len_of_wire_declare_left_val}};//rd''')

        if ( group_rd_ctrl_en or group_control_dict['wr_en'] ):
            self.control_lst.append(f'\n//{RegName}')
        if ( group_control_dict['rd_en'] ):
            self.rd_reg_lst.append(RegName)
            if group_rd_ctrl_en:
                self.control_lst.append(f'''{"wire":<4} {RegName.lower()+'_rd':<{self.max_len_of_RegName+3}} = {'( '+self.signal_p_addr+' == '+f'{RegName.upper():<{self.max_len_of_RegName}}'+' ) && apb_rd':<{self.max_len_of_wire_declare_right_val}};''')
        if ( group_control_dict['wr_en'] or group_control_dict['rd_en_wr'] ):
            self.control_lst.append(f'''{"wire":<4} {RegName.lower()+'_wr':<{self.max_len_of_RegName+3}} = {'( '+self.signal_p_addr+' == '+f'{RegName.upper():<{self.max_len_of_RegName}}'+' ) && apb_wr':<{self.max_len_of_wire_declare_right_val}};''')

        # group write when group_entire_en
        block_assign_lst = []
        block_block_lst  = []
        if ( group_entire_en ):
            if ( group_control_dict['wr_en'] ):
                if ( group_control_dict['wr_once'] ):
                    self.wire_lst.append(f'''{"reg":<4} {' ':>{self.max_len_of_port_width}} {RegName.lower()+'_wr_done':<{self.max_len_of_wire_declare_left_val}};''')
                    block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                    block_block_lst.append(f'begin')
                    block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                    block_block_lst.append(f'''{sheet.tab}{sheet.tab}{RegName+'_wr_done'} <= 'h0;''')
                    block_block_lst.append(f'{sheet.tab}else if( {RegName}_wr )')
                    block_block_lst.append(f'''{sheet.tab}{sheet.tab}{RegName+'_wr_done'} <= 'h1;''')
                    block_block_lst.append(f'end\n')

                block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                block_block_lst.append(f'begin')
                block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                block_block_lst.append(f'{sheet.tab}{sheet.tab}{wr_reg_name} <= {group_rst_val};')
                if ( group_control_dict['rd_clear'] or group_control_dict['rd_set'] ):
                    block_block_lst.append(f'{sheet.tab}else if( {RegName.lower()}_rd )')
                    block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_reg_name} <= {str(group.loc[0,"Width"])+"'h"+str(hex(int('1'*group.loc[0,"Width"],base=2))[2:] if group_control_dict['rd_set'] else 0)};''')

                if ( group_control_dict['wr_once'] ):
                    block_block_lst.append(f'{sheet.tab}else if( {RegName.lower()}_wr && ~{RegName}_wr_done )')
                    block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_reg_name} <= {self.signal_p_wr_data};''')
                else:
                    block_block_lst.append(f'{sheet.tab}else if( {RegName.lower()}_wr )')
                    block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_reg_name} <= {self.signal_p_wr_data};''')
                block_block_lst.append(f'end\n')

                # group write when group_entire_en && group_control_dict['wr_en'] && group_shadow_en
                if ( group_shadow_en_any ):
                    self.wire_lst.append(f'''{"reg":<4} [{group.Width.unique()[0]}-1:0] {RegName.lower()+self.shadow_suffix:<{self.max_len_of_wire_declare_left_val}};''')
                    block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                    block_block_lst.append(f'begin')
                    block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                    block_block_lst.append(f'{sheet.tab}{sheet.tab}{RegName.lower()+self.shadow_suffix} <= {group_rst_val};')
                    block_block_lst.append(f'{sheet.tab}else if( {self.signal_update_en} )')
                    block_block_lst.append(f'''{sheet.tab}{sheet.tab}{RegName.lower()+self.shadow_suffix} <= {wr_reg_name};''')
                    block_block_lst.append(f'end\n')

        # process every field name
        for row_index in group.index:
            control_dict    = self.parse_Access(group.loc[row_index,"FiledAccess"],group.loc[row_index,"FieldName"])
            shadow_en       = re.match(r'1[rw]{0,2}',str(group.loc[row_index,"Shadow"]).lower())
            rd_out_flag_en  = re.search(r'r',str(group.loc[row_index,"Shadow"]).lower())
            wr_out_flag_en  = re.search(r'w',str(group.loc[row_index,"Shadow"]).lower())
            output_reg      = RegName.lower()+self.shadow_suffix if shadow_en else wr_reg_name
            wr_field        = group.loc[row_index,"FieldName_Cal"]
            wr_field_shadow = group.loc[row_index,"FieldName_Cal"] + ( self.shadow_suffix if shadow_en else '' )

            if ( control_dict['wr_en'] ):
                self.port_lst.append(f'''{sheet.tab}{"output "+("" if group_entire_en else "reg"):<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')

                if ( group_entire_en ):
                    block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]:<{max_len_of_block_assign_left_val}} = {output_reg+"["+(f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else '') + f'{group.loc[row_index,"Low"]}'+']':<{max_len_of_block_assign_right_val}};''')

                    if wr_out_flag_en :
                        self.port_lst.append(f'''{sheet.tab}{"output reg":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.wr_en_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                        block_block_lst.append(f'begin')
                        block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+self.wr_en_suffix} <= 'h0;''')
                        block_block_lst.append(f'{sheet.tab}else')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+self.wr_en_suffix} <= {RegName.lower()+'_wr'};''')
                        block_block_lst.append(f'end\n')
                else:
                    if ( control_dict['wr_once'] ):
                        self.wire_lst.append(f'''{"reg":<4} {' ':>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+'_wr_done':<{self.max_len_of_wire_declare_left_val}};''')
                        block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                        block_block_lst.append(f'begin')
                        block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+'_wr_done'} <= 'h0;''')
                        block_block_lst.append(f'{sheet.tab}else if( {group.loc[row_index,"RegName"].lower()}_wr )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+'_wr_done'} <= 'h1;''')
                        block_block_lst.append(f'end\n')

                    block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                    block_block_lst.append(f'begin')
                    block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                    block_block_lst.append(f'{sheet.tab}{sheet.tab}{wr_field} <= {group.loc[row_index,"ResetValue_Cal"]};')
                    if ( control_dict['rd_clear'] or control_dict['rd_set'] ):
                        block_block_lst.append(f'{sheet.tab}else if( {RegName.lower()}_rd )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_field} <= {str(group.loc[row_index,"Len_Cal"])+"'h"+str(hex(int('1'*group.loc[row_index,"Len_Cal"],base=2))[2:] if control_dict['rd_set'] else 0)};''')

                    if ( control_dict['wr_once'] ):
                        block_block_lst.append(f'{sheet.tab}else if( {RegName.lower()}_wr && ~{group.loc[row_index,"FieldName_Cal"]}_wr_done )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_field} <= {self.signal_p_wr_data}[{f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else ''}{group.loc[row_index,"Low"]}];''')
                    else:
                        block_block_lst.append(f'{sheet.tab}else if( {RegName.lower()}_wr )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_field} <= {self.signal_p_wr_data}[{f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else ''}{group.loc[row_index,"Low"]}];''')
                    block_block_lst.append(f'end\n')

                    if shadow_en :
                        self.wire_lst.append(f'''{"reg":<4} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {wr_field_shadow:<{self.max_len_of_wire_declare_left_val}};''')
                        block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                        block_block_lst.append(f'begin')
                        block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                        block_block_lst.append(f'{sheet.tab}{sheet.tab}{wr_field_shadow} <= {group.loc[row_index,"ResetValue_Cal"]};')
                        block_block_lst.append(f'{sheet.tab}else if( {self.signal_update_en} )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{wr_field_shadow} <= {wr_field};''')
                        block_block_lst.append(f'end\n')

                    if wr_out_flag_en :
                        self.port_lst.append(f'''{sheet.tab}{"output reg":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.wr_en_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                        block_block_lst.append(f'begin')
                        block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+self.wr_en_suffix} <= 'h0;''')
                        block_block_lst.append(f'{sheet.tab}else')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+self.wr_en_suffix} <= {RegName.lower()+'_wr'};''')
                        block_block_lst.append(f'end\n')


            if ( control_dict['rd_en'] ):
                if( group.loc[row_index,"FieldName"].lower() == "reserved" ):
                    if( group_control_dict['rd_en'] ):
                        block_assign_lst.append(f'''assign {RegName.lower()+"["+(f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else '') + f'{group.loc[row_index,"Low"]}'+']':<{max_len_of_block_assign_left_val}} = {group.loc[row_index,"ResetValue_Cal"]:<{max_len_of_block_assign_right_val}};''')

                else:
                    if not( control_dict['wr_en'] ):
                        self.port_lst.append(f'''{sheet.tab}{"input":<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                    block_assign_lst.append(f'''assign {RegName.lower()+"["+(f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else '') + f'{group.loc[row_index,"Low"]}'+']':<{max_len_of_block_assign_left_val}} = {group.loc[row_index,"FieldName_Cal"]:<{max_len_of_block_assign_right_val}};''')

                    if rd_out_flag_en :
                        self.port_lst.append(f'''{sheet.tab}{"output reg":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.rd_en_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_block_lst.append(f'always @ ( posedge {self.signal_clk } or negedge {self.signal_rstn})')
                        block_block_lst.append(f'begin')
                        block_block_lst.append(f'{sheet.tab}if( ~{self.signal_rstn} )')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+self.rd_en_suffix} <= 'h0;''')
                        block_block_lst.append(f'{sheet.tab}else')
                        block_block_lst.append(f'''{sheet.tab}{sheet.tab}{group.loc[row_index,"FieldName_Cal"]+self.rd_en_suffix} <= {RegName.lower()+'_rd'};''')
                        block_block_lst.append(f'end\n')

                    if ( ( control_dict['rd_clear'] or control_dict['rd_set'] ) and not( control_dict['wr_en'] ) ):
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+(self.clr_suffix if control_dict['rd_clear'] else self.set_suffix):<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+(self.clr_val_suffix if control_dict['rd_clear'] else self.set_val_suffix):<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+(self.clr_suffix if control_dict['rd_clear'] else self.set_suffix):<{max_len_of_block_assign_left_val}} = {RegName.lower()+('_rd'):<{max_len_of_block_assign_right_val}};''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+(self.clr_val_suffix if control_dict['rd_clear'] else self.set_val_suffix):<{max_len_of_block_assign_left_val}} = {str(group.loc[row_index,"Len_Cal"])+"'h"+str(hex(int('1'*group.loc[row_index,"Len_Cal"],base=2))[2:] if control_dict['rd_set'] else 0):<{max_len_of_block_assign_right_val}};''')

                    if ( control_dict['wr_clear'] or control_dict['wr_set'] ):
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+(self.clr_suffix if control_dict['wr_clear'] else self.set_suffix):<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+(self.clr_val_suffix if control_dict['wr_clear'] else self.set_val_suffix):<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+(self.clr_suffix if control_dict['wr_clear'] else self.set_suffix):<{max_len_of_block_assign_left_val}} = {RegName.lower()+'_wr':<{max_len_of_block_assign_right_val}};''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+(self.clr_val_suffix if control_dict['wr_clear'] else self.set_val_suffix):<{max_len_of_block_assign_left_val}} = {str(group.loc[row_index,"Len_Cal"])+"'h"+str(hex(int('1'*group.loc[row_index,"Len_Cal"],base=2))[2:] if control_dict['wr_set'] else 0):<{max_len_of_block_assign_right_val}};''')

                    if ( control_dict['wr_one_clear'] or control_dict['wr_zero_clear'] ):
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.clr_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.clr_val_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+self.clr_suffix:<{max_len_of_block_assign_left_val}} = {RegName.lower()+'_wr':<{max_len_of_block_assign_right_val}};''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+self.clr_val_suffix:<{max_len_of_block_assign_left_val}} = {f'{group.loc[row_index,"FieldName_Cal"]}'+' & '+('~' if control_dict['wr_one_clear'] else '')+self.signal_p_wr_data+'['+str(f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else '')+str(group.loc[row_index,"Low"])+']':<{max_len_of_block_assign_right_val}};''')
                    elif ( control_dict['wr_one_set'] or control_dict['wr_zero_set'] ):
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.set_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+self.set_val_suffix:<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+self.set_suffix:<{max_len_of_block_assign_left_val}} = {RegName.lower()+'_wr':<{max_len_of_block_assign_right_val}};''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+self.set_val_suffix:<{max_len_of_block_assign_left_val}} = {f'{group.loc[row_index,"FieldName_Cal"]}'+' | '+('~' if control_dict['wr_zero_set'] else '')+self.signal_p_wr_data+'['+str(f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else '')+str(group.loc[row_index,"Low"])+']':<{max_len_of_block_assign_right_val}};''')
                    elif ( control_dict['wr_one_toggle'] or control_dict['wr_zero_toggle'] ):
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+'Tgl':<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        self.port_lst.append(f'''{sheet.tab}{"output":<{self.max_len_of_extend_port_direction}} {'['+f'{str(group.loc[row_index,"Len_Cal"]):>{self.max_len_of_Width}}'+"-1:0]" if group.loc[row_index,"Len_Cal"] > 1 else ' ' :>{self.max_len_of_port_width}} {group.loc[row_index,"FieldName_Cal"]+'TglVal':<{self.max_len_of_port_name+self.max_len_of_name_suffix}},''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+self.tgl_suffix:<{max_len_of_block_assign_left_val}} = {RegName.lower()+'_wr':<{max_len_of_block_assign_right_val}};''')
                        block_assign_lst.append(f'''assign {group.loc[row_index,"FieldName_Cal"]+self.tgl_val_suffix:<{max_len_of_block_assign_left_val}} = {f'{group.loc[row_index,"FieldName_Cal"]}'+' ^ '+('~' if control_dict['wr_zero_toggle'] else '')+self.signal_p_wr_data+'['+str(f'{group.loc[row_index,"High"]}'+':' if group.loc[row_index,"Len_Cal"] > 1 else '')+str(group.loc[row_index,"Low"])+']':<{max_len_of_block_assign_right_val}};''')

        self.block_lst = self.block_lst + block_assign_lst + block_block_lst

    def gen_file(self,sheet_name='',tar_file_name=''):
        self.port_lst[-1] = self.port_lst[-1].rstrip(',')
        self.port_lst.append(f');')
        self.block_lst.append(f'\nendmodule')

        with open(tar_file_name,'w') as file_obj:
            for line in self.file_header.split('\n'):
                file_obj.write(line)
                file_obj.write('\n')
            for line in self.port_lst+self.param_lst+self.wire_lst+self.control_lst+self.block_lst:
                file_obj.write(line)
                file_obj.write('\n')
        print(f'sheet {sheet_name} has been mapped successfully into {tar_file_name}!')



def arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev = True)
    parser.add_argument("-f","--filename",metavar="InputFile",dest='filename',help='Specify input xls file',nargs='+')
    parser.add_argument("-sheet",metavar="SheetName",help='To specify one sheet in the file')
    parser.add_argument("-author",metavar="Author",help='specify author of output files',default=None)
    parser.add_argument("-namerule",choices=[0,1,2],help=f'specify the naming rule of FieldName   0:auto;1:UpperCamelCase;2:under_score_case',type=int,default=0)
    parser.add_argument("-fout",metavar="OutputFile",help='specify the output file',default='')
    parser.add_argument("-ins",choices=[0,1],help='automatic instantiating switch : 0:off;1:on;',default=1)
    parser.add_argument('-v','--verbose',choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],dest='verbose',help='set logger_level',default='ERROR')

    # parser.print_help()
    args          = vars(parser.parse_args())
    file_name_lst = args["filename"]
    sheet_name    = args["sheet"]
    author        = args["author"]
    name_rule     = args["namerule"]
    tar_file_name = args["fout"]
    ins_switch    = args["ins"]
    logger_level  = args["verbose"]

    for file_name in file_name_lst:
        if not os.path.exists(file_name):
            print(f"[Error]: No such file :{file_name}")
            sys.exit(1)

    print('input file    : {}\nsheet name    : {}\nauthor        : {}\noutput file   : {}\nlogger level  : {}'.format(file_name_lst,sheet_name,author,tar_file_name,logger_level))
    return file_name_lst,sheet_name,author,name_rule,tar_file_name,ins_switch,logger_level

# --Main-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    file_name_lst,sheet_name,author,name_rule,tar_file_name,ins_switch,logger_level = arg_parser()

    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(levelname)s - %(message)s\n/-------------------------------------------------------------------------------------------',level=logger_level)

    file_list  = file_name_lst if file_name_lst else [f for f in glob.glob('*.xls')+glob.glob('*.xlsx')]
    for file in file_list:
        book = book(file,sheet_name,author,name_rule,tar_file_name)

    if ins_switch:
        print(f'''\nInstantiating...\n{'-'*60}''')
        if book.tar_file_name_lst:
            os.system(f'python ins.py -f {" ".join(book.tar_file_name_lst)}')
        else:
            os.system(f'python ins.py')
