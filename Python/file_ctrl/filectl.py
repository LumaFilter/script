#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2021-12-27 19:15:38
 $ @LastEditTime : 2022-02-27 17:34:59
 $ @LastEditors  : Luma
 $ @Description  : File Controller

 $ @FilePath     : \file_ctrl\filectl.py
'''
from pathlib import Path
import os
import re
import glob
import shutil
import collections
import argparse
import py7zr

def sort(top_path,out_top_path):
    category_list = ["01.苹果","02.桃","03.梨","04.其他"]
    for category in category_list:
        path = Path( out_top_path ) / category
        if not path.exists():
            path.mkdir(parents=True)

    for (root,dirs,files) in os.walk(top_path):
        if not re.search('统计',root):
            for file in files:
                if re.match('.*\.txt',file):
                    if re.search('苹果|秦冠|金元帅',file):
                        category = "01.苹果"
                    elif re.search('黄桃|血桃',file):
                        category = "02.桃"
                    elif re.search('砀山|梨',file):
                        category = "03.梨"
                    else:
                        category = "04.其他"

                    if not os.path.exists(os.path.join(out_top_path,category,file)):
                        shutil.move(os.path.join(root,file),os.path.join(out_top_path,category))


def rename(top_path):
    for (root,dirs,files) in os.walk(top_path):
        for file in files:
            if re.match('.*\.txt',file):
                old_name = os.path.join(root,file)
                (new_name,extension) = os.path.splitext(file)
                new_name = re.sub("pingguo|apple", "苹果", new_name)
                new_name = re.sub("peach", "桃", new_name)
                new_name = re.sub("pear", "桃", new_name)

                new_name = os.path.join(root,new_name+extension)
                try:
                    os.rename(old_name,new_name)
                except:
                    continue

def compress(source_file,destination_file):
    password = "123456"
    destination_dir = Path(destination_file).resolve()/"压缩包"
    if not destination_dir.exists():
            destination_dir.mkdir(parents=True)
    for (root,dirs,files) in os.walk(source_file):
        for file in files:
            if re.match('.*\.txt',file):
                file_path = Path(root).resolve()/file
                with py7zr.SevenZipFile(destination_dir/(file_path.stem+".7z"), mode='w',password=password) as archive:    
                    archive.write(Path(root).resolve()/file,file)
                print("{} \thave been compressed successfully!".format(Path(root).resolve()/file))

def show_dir(top_path):
    path = Path(top_path)
    dir_size = {}

    # calc dir size
    for iterdir in path.iterdir():
        if iterdir.is_dir:
            size = 0
            for (root,dirs,files) in os.walk(iterdir):
                size += sum([os.path.getsize(os.path.join(root, file)) for file in files])
            dir_size[str(iterdir)] = size/1024/1024

    # sort
    dir_size = sorted(dir_size.items(),key=lambda dir_size:dir_size[1],reverse=True)

    # print
    for dir,size in dir_size:
        print('{:<15}: {:>7.2f} Mb'.format(dir,size))

def arg_parser():
    parser = argparse.ArgumentParser(allow_abbrev = True)
    parser.add_argument("-s","-source dir",metavar="SourceDir",dest='SourceDir',default='.')
    parser.add_argument("-d","-destination dir",metavar="DestinationDir",dest='DestinationDir',default=os.path.join(os.getcwd(),"sort"))
    parser.add_argument("-coms","-comprehension source dir",metavar="ComprehensionSourceDir",dest='ComprehensionSourceDir',default=None)
    parser.add_argument("-comd","-comprehension destination dir",metavar="ComprehensionDestinationDir",dest='ComprehensionDestinationDir',default=None)

    # parser.print_help()
    options                 = vars(parser.parse_args())
    top_path                = options["SourceDir"]
    out_top_path            = options["DestinationDir"]
    com_source_file         = options["ComprehensionSourceDir"]
    com_destination_file    = options["ComprehensionDestinationDir"]

    print('input directory         : {}\noutput directory        : {}'.format(top_path,out_top_path))
    return top_path,out_top_path,com_source_file,com_destination_file


# --Main-----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    top_path,out_top_path,com_source_file,com_destination_file = arg_parser()

    sort(top_path,out_top_path)
    rename(out_top_path)
    compress(com_source_file,com_destination_file)
    show_dir(top_path)