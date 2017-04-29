#!/usr/bin/env python 
#encoding=utf8

import os
import sys
import string
import xlrd
import xlwt
import re
import glob
import shutil
#import optparse
reload(sys)
sys.setdefaultencoding('utf-8')

INI_INFO = u'''[CONNECTION:SERIAL]
Parity=0
StopBits=0
ComPort=0
BaudRate=6
FlowCtrl=0
DataBits=3
[CONNECTION]
Port=2009
Protocol=SSH
SendKeepAliveInterval=60
AutoReconnect=0
TCPKeepAlive=0
KeepAliveInterval=60
KeepAliveString=
AutoReconnectInterval=30
Host=1.1.1.1
KeepAlive=1
SendKeepAlive=0
AutoReconnectLimit=0
[Information]
Description=Xshell Session Profile
MinorVersion=0
MajorVersion=3
[CONNECTION:AUTHENTICATION]
TelnetLoginPrompt=ogin:
TelnetPasswordPrompt=assword:
ScriptPath=C:\\Users\\Administrator\\AppData\\Roaming\\NetSarang\\Xshell\\Sessions\\飞车\\正式服-S1\\game.vbs
UseExpectSend=0
UserName=wyd
UserKey=
ExpectSend_Count=0
Password=8aKERPb3qwY1iOh0Vw==
Passphrase=
UseInitScript=1
Method=0
RloginPasswordPrompt=assword:
[CONNECTION:TELNET]
NegoMode=0
Display=$PCADDR:0.0
XdispLoc=1
[USERINTERFACE]
NoQuickButton=0
ShowOnLinkBar=0
QuickCommand=
[CONNECTION:SSH]
ForwardX11=0
VexMode=0
LaunchAuthAgent=1
InitLocalDirectory=
MAC=
UseAuthAgent=0
Compression=0
Cipher=
Display=localhost:0.0
InitRemoteDirectory=
ForwardToXmanager=1
FwdReqCount=0
NoTerminal=0
CipherList=aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,arcfour,aes192-cbc,aes256-cbc,rijndael128-cbc,rijndael192-cbc,rijndael256-cbc,aes256-ctr,aes192-ctr,aes128-ctr,rijndael-cbc@lysator.liu.se
MACList=hmac-sha1,hmac-sha1-96,hmac-md5,hmac-md5-96,hmac-ripemd160,hmac-ripemd160@openssh.com
[TERMINAL]
ScrollErasedText=1
DisableTitleChange=0
IgnoreResizeRequest=0
UseInitSize=0
DisableBlinkingText=0
ShiftForcesLocalUseOfMouse=1
ForceEraseOnDEL=0
KeyMap=0
InitReverseMode=0
DeleteSends=0
BackspaceSends=2
UseAltAsMeta=0
InitKeypadMode=0
InitCursorMode=0
AltKeyMapPath=
CtrlAltIsAltGr=1
DisableTermPrinting=0
ScrollBottomOnKeyPress=0
InitInsertMode=0
Type=xterm
Rows=24
CodePage=65001
ScrollbackSize=1024
InitNewlineMode=0
InitEchoMode=0
CJKAmbiAsWide=1
InitOriginMode=0
DisableAlternateScreen=0
ScrollBottomOnTermOutput=1
InitAutoWrapMode=1
RecvLLAsCRLF=0
Cols=80
EraseWithBackgroundColor=1
[LOGGING]
AutoStart=0
Type=0
FilePath=
Overwrite=1
FileMethod=0
[CONNECTION:FTP]
Passive=1
InitLocalDirectory=
InitRemoteDirectory=
[CONNECTION:PROXY]
StartUp=0
Proxy=
[TERMINAL:WINDOW]
FontSize=12
CharSpace=0
CursorBlink=0
LineSpace=0
FontFace=Courier New
BoldMethod=2
ColorScheme=ANSI Colors on Black
CursorAppearance=0
arginLeft=2
CursorTextColor=0
MarginBottom=2
MarginTop=2
MarginRight=2
CursorColor=65280
CursorBlinkInterval=600
[TRANSFER]
FolderMethod=0
SendFolderPath=
FolderPath=
DuplMethod=0
AutoZmodem=1
[CONNECTION:RLOGIN]
TermSpeed=38400
[TRACE]
SshTunneling=0
SshLogin=0
SockConn=1
TelnetOptNego=0
'''

#dirpath="/data/host/dir/"                               #定义操作目录
listid=[10001,10002,10003,10004,20001,20002,20003,20004,30001,30002,30003,40001,40002]

def read_excel(num):
    '''
    Get colunn data,return list
    '''
    workbook = xlrd.open_workbook(r'/data/host/host.xlsx')
    sheet4 =  workbook.sheet_by_index(4)
#    print sheet4.name,sheet4.nrows,sheet4.ncols
#    print sheet4.cell(24,3).value.encode('utf-8')    # 获取单元格内容 
    cols = sheet4.col_values(num)                     # 获取第num列内容(数组) 
    name=[]
    for index in cols:
        if index != '' and index != " ":
            name.append(index)
    return name;

def mkdir_name():
    '''
    create directory about server-name
    '''
    os.chdir(dirpath)
    list = read_excel(num=2)
    for dirname in list[1:]:
#        print dirname
        dir = "S1" + "-" + str(dirname)
        if os.path.exists(dir):
            shutil.rmtree(dir)
            print "delete success"
            os.mkdir(dir)
        if not os.path.exists(dir):
         os.mkdir(dir)

#获取所有的公网ip地址
def publicip(num=8):     		 #默认第8列
    '''
    Get all host public ip
    '''
    cols = read_excel(num)
    ip = []
    for index in cols:
        matchObj = re.match('\d',index)
        if matchObj:
            ip.append(index)
        else:
            pass
#    print ip
    return ip

#获取所有的minion-id
def minionid(num=10):             	#默认第10列
    '''
    Get all minion id name
    '''
    minion_id = read_excel(num)
    id = []
    for index in minion_id:
        matchObj = re.match('S1',index)
        if matchObj:
            id.append(index)
        else:
            pass
#    print id
    return id

def sessions(colip,colname):               		 #参数1为公网ip所在的行,参数2为session的名字
    '''
    create session about xshell
    '''
    hostip = publicip(colip)
    sessionname = minionid(colname)
    xshell = dict(zip(sessionname,hostip))    		 #主机名及ip对应的字典
#    print xshell
    os.chdir(dirpath)
    for key, value in xshell.items():
        xshellname = key + ".xsh"
        info = string.replace(INI_INFO,'1.1.1.1',str(value))
        fp = open(xshellname, "w")
        fp.write(info.encode("gbk"))
        fp.close()
    print "create xshell file done,please check!"

def mvsessions():
    '''
    move xshell file to server-id dir
    '''
    sessionname = glob.glob(dirpath + '*.xsh')         #找出目录下所有的xsh文件
    for name in sessionname:
        if 'Room' in name or 'Scenemgr' in name:
#            print name
            shutil.move(name,dirpath + "S1-全局")
        for serverid in listid:
            if str(serverid) in name:
                shutil.move(name,dirpath  + "S1" + "-" + str(serverid) + ".0")
def main(): 
    mkdir_name()
    sessions(colip=8,colname=10)
    mvsessions()

if __name__ == "__main__":
    dirpath="/data/host/dir/"                               #定义操作目录
    main()
