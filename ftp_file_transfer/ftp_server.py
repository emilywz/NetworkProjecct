"""
FTP 文件服务器
"""
from time import *
from socket import *
from threading import Thread
from model import *
import os, sys


class FTPServerHandleRequest(Thread):
    """
    服务端查看列表,下载,上传,退出处理
    """

    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd
        self._pro = ProtocalModel()

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == self._pro.Quit:
                return
            elif data == self._pro.FileList:
                self.check_list()
            elif data.strip()[0] == self._pro.DownloadFile:
                filename = data.strip().split(" ")[-1]
                self.download_file(filename)
            elif data.strip()[0] == self._pro.UploadFile:
                filename = data.strip().split(" ", 1)[-1]
                self.upload_file(filename)

    def check_list(self):
        """
        查看文件库文件
        :param connfd:连接套接字
        """
        files = os.listdir(self._pro.FTPFilePath)
        if not files:
            self.connfd.send("No files".encode())
            return
        else:
            self.connfd.send(self._pro.VerifyMsg.encode())

        # 拼接所有文件名
        filelist = ''
        for file in files:
            if file[0] != "." and os.path.isfile(self._pro.FTPFilePath + file):
                filelist += file + "\n"

        self.connfd.send(filelist.encode())

    def download_file(self, filename):
        """
        下载文件
        :param filename: 目标文件
        :return:
        """
        try:
            f = open(self._pro.FTPFilePath + filename, "rb")
        except Exception:
            self.connfd.send("No such file".encode())
            return
        else:
            self.connfd.send(self._pro.VerifyMsg.encode())
            sleep(0.1)

        while True:
            data = f.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(self._pro.MsgFlag.encode())
                break
            self.connfd.send(data)

        f.flush()
        f.close()

    def upload_file(self, filename):
        """
        上传文件
        :param filename: 目标文件
        """
        if os.path.exists(self._pro.FTPFilePath + filename):
            self.connfd.send("File exist,please reselect".encode())
            return
        else:
            self.connfd.send(self._pro.VerifyMsg.encode())

        # 接收文件
        sleep(0.1)
        with open(self._pro.FTPFilePath + filename, "wb") as f:
            while True:
                data = self.connfd.recv(1024)
                if data == self._pro.MsgFlag.encode():
                    return
                f.write(data)


class FTPServer:
    """
    FTP服务端操作
    """

    def __init__(self):
        self._sock = SocketModel()
        self._pro = ProtocalModel()
        self.list_client = []
        self.sockfd = socket()

    def create_socket(self):
        """
        创建套接字
        """
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self._sock.Server_ADDR)

        self.sockfd.listen(3)
        print("Listen the post %s ..." % self._sock.PORT)

    def tcp_server(self):
        """
        服务端运行
        """
        self.create_socket()

        while True:
            # 循环接收客户端连接
            try:
                connfd, addr = self.sockfd.accept()
                print("Connect from...", addr)
            except KeyboardInterrupt:
                sys.exit("Server Disconnect...")
            except Exception:
                print(Exception)
                continue

            # 创建线程
            t = FTPServerHandleRequest(connfd)
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    ftp = FTPServer()
    ftp.tcp_server()
