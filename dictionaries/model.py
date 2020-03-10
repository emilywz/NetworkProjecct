"""
常量,协议模块
"""

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