#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2023-09-29 18:26:52
 $ @LastEditTime : 2023-10-07 20:17:10
 $ @LastEditors  : Luma
 $ @Description  :    

 $ @FilePath     : \working\script\Python\contents\contents.py
'''
import os
import re
import glob
import logging
import argparse

import re

def process(input_file,output_file,base_value):

    # 使用正则表达式匹配章节标题和页号
    pattern = r'(§?(?:第\w+章|\d+(?:\.\d+)+|习题|练习|附录|参考|索引|综述)(?:\n?.*?)+?)(\d+)$'

    # 打开输入文件并读取整个内容为一个字符串
    with open(input_file, "r", encoding="utf-8") as input_f:
        input_text = input_f.read()

    # 使用正则表达式匹配多行目录条目
    matches = re.findall(pattern, input_text,flags=re.MULTILINE)
    logging.info(f'matches\n:{matches}')

    # 打开输出文件并写入结果
    with open(output_file, "w", encoding="utf-8") as output_f:
        for idx, (entry, page) in enumerate(matches, start=1):
            page_with_base = int(page) + base_value - 1
            entry = entry.replace('\n', ' ')
            entry = re.sub(r'[\.·]{2,}|…', '', entry)
            output_line = f"{entry.strip()} {page_with_base}\n"
            logging.debug(f'output_line\n:{output_line}')
            output_f.write(output_line)



def arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev = True)
    parser.add_argument("-f","--filename",metavar="InputFile",dest='filename',nargs='+')
    parser.add_argument("-fout",metavar="OutputFile",help='specify the output file',default='output.txt')
    parser.add_argument("-base",metavar="base value",help='base value',type=int,default=1)
    parser.add_argument('-v','--verbose',choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],dest='verbose',help='set logger_level',default='ERROR')
    parser.add_argument('-log',help='output log to log file',action='store_true')

    # parser.print_help()
    options       = vars(parser.parse_args())
    file_name_lst = options["filename"]
    tar_file_name = options["fout"]
    base_value    = options["base"]
    logger_level  = options["verbose"]
    logger_log    = options["log"]
    print('input file    : {}\noutput file   : {}'.format(file_name_lst,tar_file_name))
    return file_name_lst,tar_file_name,base_value,logger_level,logger_log

# --Main-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    file_name_lst,tar_file_name,base_value,logger_level,logger_log = arg_parser()

    logger = logging.getLogger(__name__)
    if logger_log:
        logging.basicConfig(format = '%(levelname)s - %(message)s\n/-------------------------------------------------------------------------------------------',level=logger_level,filename='ins.log',filemode='w')
    else:
        logging.basicConfig(format = '%(levelname)s - %(message)s\n/-------------------------------------------------------------------------------------------',level=logger_level)


    file_list  = file_name_lst if file_name_lst else [f for f in glob.glob('*.txt') if not re.match(r'output.txt', f)]
    for file in file_list:
        process(file,tar_file_name,base_value)
