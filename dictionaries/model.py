#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#Author:Emily_Wang
#evn:python3.6

class SocketModel:
    HOST = "0.0.0.0"
    PORT = 2323
    Server_ADDR = (HOST, PORT)

class ProtocolModel:
    Login = "LIN"
    Register = "R"
    Logoff = "LOFF"
    Quit="Q"
    LookupWord="LWORD"
    History="H"
    MsgFlag = "##"
    VerifyMsg = "OK"
    FailMsg="FAIL"
