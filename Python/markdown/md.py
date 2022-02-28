#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2022-01-19 21:21:16
 $ @LastEditTime : 2022-02-28 15:16:43
 $ @LastEditors  : Luma
 $ @Description  : markdown standardize

 $ @FilePath     : \MarkDown\md.py
'''
import os
import re
import logging
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',level=logging.DEBUG)
# logger.warning('waring，用来用来打印警告信息')
# logger.error('error，一般用来打印一些错误信息')
# logger.critical('critical，用来打印一些致命的错误信息，等级最高')


def arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev = True)
    parser.add_argument("input_file",default='.')

    # parser.print_help()
    options                 = vars(parser.parse_args())
    input_file              = os.path.abspath(options["input_file"])

    print('input file         : {}\n'.format(input_file))
    return input_file

def md_linefeed_and_indentation(input_file='.'):
    with open(input_file,'r',encoding='UTF-8') as f_r,open(input_file+'.bak','w',encoding='UTF-8') as f_w:
        f_w.write('<font size=3>'+'\n\n')
        line_cnt  = 0
        code_flag = 0
        for line in f_r:
            if ( line.strip() != '' ):
                if ( line_cnt > 7):
                    if re.match(r'^```\w*\s*$',line.strip()):           #代码块
                        code_flag = code_flag ^ 1
                        line = "\n" + line.strip() + "    \n\n"
                    elif code_flag == 0:
                        if line.strip().startswith('#'):                #标题
                            line = "\n" + line.strip() + "    \n\n"
                        elif line.strip().startswith(('-','+','*')):    #无序列表或分隔线
                            line = line.rstrip() + "    \n"
                        elif re.match(r'^<.*>$',line.strip()):          #图片、字体等设置
                            line = line.strip() + "    \n"
                        elif line.strip().startswith('> '):             #引用
                            line = line.rstrip() + "    \n"
                        elif re.match(r'^\[.*\]\(.*\)$',line.strip()):  #链接
                            line = line.rstrip() + "    \n"
                        else:
                            line = "&emsp;&emsp;" + line.strip() +  "    \n"
                f_w.write(line)
                line_cnt += 1
            else:
                f_w.write('\n')
        f_w.write('\n'+'</font>')

    os.remove(input_file)
    os.rename(input_file+'.bak',input_file)

def md_add_blankline(input_file='.'):
    with open(input_file,'r',encoding='UTF-8') as f_r,open(input_file+'.bak','w',encoding='UTF-8') as f_w:
        line_cnt = 0
        for line in f_r:
            if ( line.strip() != '' ):
                if ( line_cnt > 8):
                    line = line + "\n"
                f_w.write(line)
                line_cnt += 1
            else:
                f_w.write('\n')

# --Main-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    input_file = arg_parser()
    md_linefeed_and_indentation(input_file)
    md_add_blankline(input_file)





#> [Python实用教程系列——Logging日志模块](https://zhuanlan.zhihu.com/p/166671955)   
#> [Python中使用logging模块代替print（logging简明指南）](https://www.jb51.net/article/52022.htm)   
#> [python--文件操作删除某行](https://blog.csdn.net/qq_31135027/article/details/78908559)   
#> [Python-文件读写及修改](https://www.cnblogs.com/zhxwind/p/8761618.html#:~:text=Python-%E6%96%87%E4%BB%B6%E8%AF%BB%E5%86%99%E5%8F%8A%E4%BF%AE%E6%94%B9%20%E6%96%87%E4%BB%B6%E7%9A%84%E8%AF%BB%E5%86%99%E6%9C%89%E4%B8%89%E7%A7%8D%E5%BD%A2%E5%BC%8F%EF%BC%9A%E8%AF%BB%E3%80%81%E5%86%99%E5%92%8C%E8%BF%BD%E5%8A%A0%E3%80%82%20%E4%B8%80%E3%80%81%E8%AF%BB%E6%A8%A1%E5%BC%8F%20r%20%E5%92%8C%E8%AF%BB%E5%86%99%E6%A8%A1%E5%BC%8F,r%2B%201%E3%80%81%E8%AF%BB%E6%A8%A1%E5%BC%8F%20r%20%E8%AF%BB%E6%A8%A1%E5%BC%8Fr%E7%89%B9%E7%82%B9%EF%BC%9A%EF%BC%881%EF%BC%89%E5%8F%AA%E8%83%BD%E8%AF%BB%EF%BC%8C%E4%B8%8D%E8%83%BD%E5%86%99%EF%BC%9B%EF%BC%882%EF%BC%89%E6%96%87%E4%BB%B6%E4%B8%8D%E5%AD%98%E5%9C%A8%E6%97%B6%E4%BC%9A%E6%8A%A5%E9%94%99%E3%80%82%20%EF%BC%881%EF%BC%89%E4%BE%8B%EF%BC%9A%E8%AF%BB%E5%8F%96%E5%BD%93%E5%89%8D%E7%9B%AE%E5%BD%95%E4%B8%8B%E7%9A%84books.txt%E6%96%87%E4%BB%B6%EF%BC%8C%E8%AF%A5%E6%96%87%E4%BB%B6%E5%A6%82%E4%B8%8B%E6%89%80%E7%A4%BA%E3%80%82)   
#> [python seek()和tell()函数简介](https://blog.csdn.net/lwgkzl/article/details/81058529?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2.pc_relevant_default&utm_relevant_index=5)   
#> [endswith()匹配多种结尾的方式](https://blog.csdn.net/Homewm/article/details/90644022?spm=1001.2101.3001.6650.8&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-8.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-8.pc_relevant_default&utm_relevant_index=13)   
#> [5种Python逐行读取文件的方式](https://blog.csdn.net/qdPython/article/details/106160272)   