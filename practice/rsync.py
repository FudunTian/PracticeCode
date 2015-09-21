# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os,re
import subprocess
import platform
import traceback
from PyQt4 import QtGui,QtCore
import ctypes
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

PLAT = platform.system()

RSYNC_EXEC_WIN = 'S:/app/win/rsync/rsync.exe'
RSYNC_DEFAULT_ARGS = '-aPz'
RSYNC_EXEC_LIN = 'rsync'

def _MountDriver(address,password,username):
    c = address.split("\\")
    iP_address = r"\\"
    iP_address = iP_address+c[2]+"\\"+c[3]
    l = len(c)
    e = l -  4

    lpBuffer = ctypes.create_string_buffer(78)
    ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
    vol = lpBuffer.raw.split('\x00')
    used_div = list()
    div=[ 'C:\\', 'D:\\', 'E:\\', 'R:\\', 'T:\\', 'Y:\\', 'U:\\', 'I:\\', 'O:\\', 'P:\\',
            'S:\\', 'F:\\', 'G:\\', 'H:\\', 'J:\\', 'K:\\', 'L:\\', 'Z:\\', 'X:\\', 'V:\\',
            'N:\\', 'M:\\',]
    for i in vol:
        if i:
            used_div.append(i)
    un_div = list(set(div).difference(set(used_div)))
    print un_div
    amounted  = str(un_div[1])
    use_amount = amounted.strip(r"\\")
    run = "net use "+use_amount +" "+iP_address+" "+'""'+" "+"/USER:"+username
    print run
    if password.strip()== "":
        prog = subprocess.check_call (str("net use "+use_amount +" "+iP_address+" "+'""'+" "+"/USER:"+username),
                                    stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell=True)

    else:
        prog = subprocess.check_call (str("net use "+use_amount +" "+iP_address+" "+password+" "+"/USER:"+username),
                                    stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)

    for i in range(e):
        amounted = amounted + c[4+int(i)]+"\\"
    return amounted

def _modify(address):
    address = address.replace("\\","/")
    address = "/cygdrive/" + address
    address =  address.replace(":","")
    return address


def rsync(src, dst,
          extra_args = [],
          src_username = '',
          src_password = '',
          dst_username = '',
          dst_password = '',
          force_mount = False ):
    pattern = re.compile(r'(\\\\(\d+\.){3}\d+)(\\\w+)')
    
    if pattern.match(src) and force_mount == True:
        src =_MountDriver(src,src_password,src_username)
        src = src.replace("\\","/")
        src = "/cygdrive/" + src
        src =  src.replace(":","")
    elif PLAT == "Windows" and (os.path.isdir(src) or os.path.isfile(src)):
        src = src.replace("\\","/")
        src = "/cygdrive/" + src
        src =  src.replace(":","")
    elif PLAT == "Linux" and (os.path.isdir(src) or os.path.isfile(src)):
        src = src.replace("\\","/")
        src =  src.replace(":","")
    else:
        raise ValueError, 'force_mount first/Can not find this dir'
        
    if pattern.match(dst)and force_mount == True:
        dst = _MountDriver(dst,dst_password,dst_username)
        dst = dst.replace("\\","/")
        dst = "/cygdrive/" + dst
        dst =  dst.replace(":","")
    elif PLAT == "Windows" and (os.path.isdir(dst) or os.path.isfile(dst)):
        dst = dst.replace("\\","/")
        dst = "/cygdrive/" + dst
        dst =  dst.replace(":","")
    elif PLAT == "Linux" and (os.path.isdir(dst) or os.path.isfile(dst)):
        dst = dst.replace("\\","/")
        dst =  dst.replace(":","")
    else:
        raise Exception("force_mount first/Can not find this dir")
    r_args = list()
    if PLAT ==  "Windows":
        r_args.append(RSYNC_EXEC_WIN)
    else:
        r_args.append(RSYNC_EXEC_LIN)
        
    r_args.append(RSYNC_DEFAULT_ARGS)
    r_args.extend(extra_args)
    r_args.append(str(src))
    r_args.append(str(dst))
    subprocess.check_call (r_args)
