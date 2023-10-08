#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2022-01-19 21:21:16
 $ @LastEditTime : 2023-10-08 13:29:08
 $ @LastEditors  : Luma
 $ @Description  : markdown standardize

 $ @FilePath     : \working\script\Python\markdown\md.py
'''
import os
import re
import logging
import argparse
from pathlib import Path


def md_linefeed_and_indentation(input_file='.',numbering=True,image_host_url_prefix=None):

    file_name = Path(input_file).stem

    # 定义计数器
    num_counters = [0, 0, 0, 0, 0, 0]
    # 使用正则表达式匹配标题，并为标题添加计数器
    def add_header_counters(match):
        level = len(match.group(1))
        num_counters[level-1] += 1
        num_counters[level:] = [0] * (6 - level)
        header_number = ".".join(str(num_counters[i]) for i in range(level))
        return f"{match.group(1)} {header_number} {match.group(2)}"

    with open(input_file,'r',encoding='UTF-8') as f_r,open(input_file+'.bak','w',encoding='UTF-8') as f_w:
        # f_w.write('<font size=3>'+'\n\n')
        line_cnt  = 0
        code_flag = 0
        for line in f_r:
            if ( line.strip() != '' ):
                if ( line_cnt > 7):
                    if re.match(r'^```\w*\s*$',line.strip()):               #代码块
                        logging.debug(f'代码块:{line}')
                        code_flag = code_flag ^ 1
                        line = "\n" + line.strip() + "    \n\n"
                    elif code_flag == 0:
                        if line.strip().startswith('#'):                    #标题
                            logging.debug(f'标题:{line}')
                            if numbering:
                                line = re.sub(r"^(#{1,6})\s+(.+)$", add_header_counters, line)
                            line = "\n" + line.strip() + "    \n\n"
                        elif line.strip().startswith(('-','+','*')):        #无序列表或分隔线
                            logging.debug(f'无序列表或分隔线:{line}')
                            line = line.rstrip() + "    \n"
                        elif re.match(r'\!\[.*?\]\(.*?\).*',line.strip()):  #图片
                            logging.debug(f'图片:{line}')
                            line = line.replace(r'./imgs/', f"{image_host_url_prefix}/{file_name}/")
                            line = line.strip() + "    \n"
                        elif re.match(r'^<.*>$',line.strip()):              #图片、字体等设置
                            logging.debug(f'图片、字体等设置:{line}')
                            line = line.strip() + "    \n"
                        elif line.strip().startswith('> '):                 #引用
                            logging.debug(f'引用:{line}')
                            line = line.rstrip() + "    \n"
                        elif re.match(r'^\[.*\]\(.*\)$',line.strip()):      #链接
                            logging.debug(f'链接:{line}')
                            line = line.rstrip() + "    \n"
                        elif not re.match(r'^&emsp;&emsp;',line.strip()):
                            logging.debug(f'正文:{line}')
                            line = "&emsp;&emsp;" + line.strip() +  "    \n"
                f_w.write(line)
                line_cnt += 1
            else:
                f_w.write('\n')


    with open(input_file,'r',encoding='UTF-8') as f_r,open(input_file+'.wechat.bak','w',encoding='UTF-8') as f_w:
        line_cnt  = 0
        code_flag = 0
        for line in f_r:
            if ( line.strip() != '' ):
                if ( line_cnt > 7):
                    if re.match(r'^```\w*\s*$',line.strip()):                   #代码块
                        logging.debug(f'代码块:{line}')
                        code_flag = code_flag ^ 1
                        line = "\n" + line.strip() + "    \n\n"
                    elif code_flag == 0:
                        if line.strip().startswith('#'):                        #标题
                            logging.debug(f'标题:{line}')
                            if numbering:
                                line = re.sub(r"^(#{1,6})\s+(.+)$", add_header_counters, line)
                            line = "\n" + line.strip() + "    \n\n"
                        elif line.strip().startswith(('-','+','*')):            #无序列表或分隔线
                            logging.debug(f'无序列表或分隔线:{line}')
                            line = line.rstrip() + "    \n"
                        elif re.match(r'\!\[.*?\]\(.*?\).*',line.strip()):      #图片
                            logging.debug(f'图片:{line}')
                            line = line.replace(r'./imgs/', f"{image_host_url_prefix}/{file_name}/")
                            line = line.strip() + "    \n"
                        elif re.match(r'^<.*>$',line.strip()):                  #图片、字体等设置
                            logging.debug(f'图片、字体等设置:{line}')
                            line = line.strip() + "    \n"
                        elif line.strip().startswith('> '):                     #引用
                            logging.debug(f'引用:{line}')
                            line = line.rstrip() + "    \n" + ( ("&emsp;&emsp;" + re.findall(r'\[.*?\]\((.*?)\)', line)[0] + "    \n") if re.findall(r'\[.*?\]\((.*?)\)', line) else '' )
                        elif re.match(r'.*?\[.+?\]\(.+?\).*?',line.strip()):    #链接
                            logging.debug(f'链接:{line}')
                            line = "&emsp;&emsp;" + line.rstrip() + "    \n" + ( ("&emsp;&emsp;" + re.findall(r'\[.*?\]\((.*?)\)', line)[0] + "    \n") if re.findall(r'\[.*?\]\((.*?)\)', line) else '' )
                        elif not re.match(r'^&emsp;&emsp;',line.strip()):
                            logging.debug(f'正文:{line}')
                            line = "&emsp;&emsp;" + line.strip() +  "    \n"
                f_w.write(line)
                line_cnt += 1
            else:
                f_w.write('\n')


def arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev = True)
    parser.add_argument("-f","--filename",metavar="input_file",dest='input_file',default='.')
    parser.add_argument("-num","--numbering",dest='numbering',action="store_false")
    parser.add_argument('-v','--verbose',choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'],dest='verbose',help='set logger_level',default='ERROR')
    parser.add_argument('-log',help='output log to log file',action='store_true')

    # parser.print_help()
    options                 = vars(parser.parse_args())
    input_file              = os.path.abspath(options["input_file"])
    numbering               = options["numbering"]
    logger_level            = options["verbose"]
    logger_log              = options["log"]

    print('input file   : {}'.format(input_file))
    print('output file1 : {}.bak'.format(input_file))
    print('output file2 : {}.wechat.bak'.format(input_file))
    return input_file,numbering,logger_level,logger_log

# --Main-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    input_file,numbering,logger_level,logger_log = arg_parser()

    logger = logging.getLogger(__name__)
    if logger_log:
        logging.basicConfig(format = '%(levelname)s - %(message)s\n/-------------------------------------------------------------------------------------------',level=logger_level,filename='ins.log',filemode='w')
    else:
        logging.basicConfig(format = '%(levelname)s - %(message)s\n/-------------------------------------------------------------------------------------------',level=logger_level)

    image_host_url_prefix = 'https://img-host.aliyuncs.com/imgs'

    md_linefeed_and_indentation(input_file,numbering,image_host_url_prefix)
