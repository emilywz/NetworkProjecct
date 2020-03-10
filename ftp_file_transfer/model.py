from socket import *


class SocketModel:
    HOST = "0.0.0.0"
    PORT = 2323
    Server_ADDR = (HOST, PORT)


class ProtocalModel:
    FTPFilePath="/home/tarena/code/FTP/"
    FileList = "L"
    DownloadFile = "D"
    UploadFile = "U"
    Quit = "Q"
    MsgFlag="###"
    VerifyMsg="OK"
