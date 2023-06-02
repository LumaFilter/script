#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2023-06-01 09:54:20
 $ @LastEditTime : 2023-06-02 09:55:04
 $ @LastEditors  : Luma
 $ @Description  :    

 $ @FilePath     : \working\script\Python\file_ctrl\pic.py
'''
# 非原创，来源：https://zhuanlan.zhihu.com/p/381152041

import os
import glob
import argparse
from pathlib import Path
import fitz # pip install PyMuPDF

#使用fitz 库直接提取pdf的图像
def muExtractImages(file_name,output_file):

    # pdf = os.path.join(Path(in_file_path).resolve(),file)
    pdf = os.path.join(in_file_path,file)
    print(pdf)

    # 打开pdf，打印PDF的相关信息
    doc = fitz.open(pdf)
    # 图片计数
    imgcount = 0
    lenXREF = doc.xref_length()    #获取pdf文件对象总数

    # 打印PDF的信息
    print("文件名:{}, 页数: {}, 对象: {}".format(pdf, len(doc), lenXREF - 1))

    pic_path = Path( output_file ) / Path( file_name ).stem
    if not pic_path.exists():
        pic_path.mkdir(parents=True)
    os.system('rm '+'\''+str(pic_path)+'\''+'/*')

    #遍历doc，获取每一页
    for page in doc:
        try:
            imgcount +=1
            tupleImage = page.get_images()
            lstImage = list(tupleImage)
            for xref in list(tupleImage):
                xref = list(xref)[0]
                # print("imgID:    %s" % imgcount)
                # print("xref:  %s" % xref)
                img = doc.extract_image(xref)   #获取文件扩展名，图片内容 等信息
                imageFilename = ("%s-%s." % (imgcount, xref) + img["ext"])
                imageFilename = imageFilename  #合成最终 的图像的文件名
                imageFilename = os.path.join(pic_path, imageFilename)   #合成最终图像完整路径名
                print(imageFilename)
                imgout = open(imageFilename, 'wb')   #byte方式新建图片
                imgout.write(img["image"])   #当前提取的图片写入磁盘
                imgout.close
        except:
            continue

def arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev = True)
    # metavar — 在 *usage说明*中的参数名称，对于必选参数默认就是参数名称，对于可选参数默认是全大写的参数名称.(和choice同时设置时只显示metavar)
    # dest — 解析后的参数名称，默认情况下，对于可选参数选取 *最长* 的名称，中划线转换为下划线.（即index)
    # 默认参数类型时str
    parser.add_argument("-f","--filename",metavar="InputFile",dest='filename',nargs='+')
    parser.add_argument("-s","-source dir",metavar="SourceDir",dest='SourceDir',default='.')
    parser.add_argument("-o","-output dir",metavar="OutputDir",dest='OutputDir',default='')


    # parser.print_help()
    options       = vars(parser.parse_args())
    file_name_lst = options["filename"]
    in_file_path  = options["SourceDir"]
    out_file_path = options["OutputDir"] if options["OutputDir"] else in_file_path
    return file_name_lst,in_file_path,out_file_path


if __name__ == '__main__':
    file_name_lst,in_file_path,out_file_path = arg_parser()
    file_list  = file_name_lst if file_name_lst else [f for f in glob.glob('*.pdf')]
    for file in file_list:
        muExtractImages(file, out_file_path)