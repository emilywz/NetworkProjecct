#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author:Emily_Wang
#evn:python3.6

from socket import *

class SocketModel:
    HOST = "0.0.0.0"
    PORT = 2323
    Server_ADDR = (HOST, PORT)


class ProtocalModel:
    FTPFilePath="../code/FTP/"
    FileList = "L"
    DownloadFile = "D"
    UploadFile = "U"
    Quit = "Q"
    MsgFlag="###"
    VerifyMsg="OK"
