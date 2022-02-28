#!/usr/bin/env python
# coding=utf-8
'''
 $ @Author       : Luma
 $ @Date         : 2021-12-28 19:51:40
 $ @LastEditTime : 2022-02-27 17:38:22
 $ @LastEditors  : Luma
 $ @Description  : M3U8 to MP4

 $ @FilePath     : \file_ctrl\m3u8.py
'''
import sys
import os
import re
import glob
import shutil
import numpy as np
import logging
import time


def merge_ts(file_path,o_file_path):
    boxer        = os.listdir(file_path)

    # suffix
    boxer_suffix = [os.path.splitext(file)[1] for file in boxer]
    file_suffix  = max(boxer_suffix,key=boxer_suffix.count)
    boxer  = [file for file in boxer if(os.path.splitext(file)[1] == file_suffix)]

    # to find mean of boxer
    file_num_bits = len(str(len(boxer)))
    avg   = int(np.ceil(np.mean([len(str(file)) for file in boxer]) if len(boxer) > 0 else 0))
    boxer = list(set(boxer).difference(set([file for file in boxer if( (abs(len(str(file)) - avg ) > file_num_bits) or (file.startswith('.')))])))
    avg     = int(np.ceil(np.mean([len(str(file.split('.')[0])) for file in boxer]) if len(boxer) > 0 else 0))
    boxer   = list(set(boxer).difference(set([file for file in boxer if abs(len(str(file.split('.')[0])) - avg ) > (file_num_bits - 1)])))

    # sort
    file_num_bits = len(str(len(boxer)-1))
    max_len = max([len(str(file.split('.')[0])) for file in boxer]) if len(boxer) > 0 else 0
    boxer   = [file for file in boxer if re.match('^[0-9]',file.split('.')[0][max_len-file_num_bits:])]
    file_num_bits = len(str(len(boxer)-1))
    max_len = max([len(str(file.split('.')[0])) for file in boxer]) if len(boxer) > 0 else 0
    boxer.sort(key=lambda fname:int(fname.split('.')[0][max_len-file_num_bits:]))

    # prefix
    prefix = boxer[0].split('.')[0][:max_len-file_num_bits]
    if( prefix != '' and (len(boxer) > 500) ):
        for file in boxer:
            os.rename(file,file.split('.')[0][max_len-file_num_bits:])
        boxer = [file.split('.')[0][max_len-file_num_bits:] for file in boxer]

    # cmd
    cmd_str    = '+'.join(boxer)
    exec_str   = "copy /b " + cmd_str + ' ' + o_file_path + '>nul'
    print("copy /b " + cmd_str + ' ' + o_file_path)
    os.system(exec_str)

# --Main-----------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    top_path = os.path.abspath('.')

    for (root,dirs,files) in os.walk(top_path):
        # 进度条
        barLen   = 20  # 进度条的长度
        task_num = len(dirs)
        done_num = 0
        t0 = time.time()

        for dir in dirs:
            if not dir.startswith('.'):
                os.rename(dir,dir.replace(' ',''))
                file_path   = os.path.join(root,dir)
                o_file_path = os.path.join(top_path,dir.split('.')[0]+'.mp4')
                os.chdir(file_path)
                try:
                    boxer = merge_ts(file_path,o_file_path)
                except Exception as e:
                    logging.exception(e)
                    continue
                os.chdir(top_path)
                shutil.move(os.path.join(root,dir),os.path.join('..','M3U8-Done'))

                # 进度条
                done_num += 1
                perFin = done_num/task_num
                numFin = round(barLen*perFin)
                numNon = barLen-numFin
                runTime = time.time() - t0
                # leftTime = (1-perFin)*(runTime/perFin)
                print(
                    f"{done_num:0>{len(str(task_num))}}/{task_num}",
                    f"|{'█'*numFin}{' '*numNon}|",
                    f"任务进度: {perFin*100:.2f}%",
                    f"已用时间: {runTime:.2f}S",
                    # f"剩余时间: {leftTime:.2f}S",
                    end='\r')