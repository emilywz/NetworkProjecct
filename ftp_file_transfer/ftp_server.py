"""
FTP_file_transfer server
evn:python3.6
"""
from time import *
from socket import *
from threading import Thread
from model import *
import os, sys


class FTPServerHandleRequest(Thread):
    """
    server:
    check file list
    upload file
    download file
    exit server
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
        check file list
        :param connfd: connection socket
        """
        files = os.listdir(self._pro.FTPFilePath)
        if not files:
            self.connfd.send("No files".encode())
            return
        else:
            self.connfd.send(self._pro.VerifyMsg.encode())

        filelist = ''
        for file in files:
            if file[0] != "." and os.path.isfile(self._pro.FTPFilePath + file):
                filelist += file + "\n"

        self.connfd.send(filelist.encode())

    def download_file(self, filename):
        """
        download file
        :param filename: target file
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
        upload file
        :param filename: target file
        """
        if os.path.exists(self._pro.FTPFilePath + filename):
            self.connfd.send("File exist,please reselect".encode())
            return
        else:
            self.connfd.send(self._pro.VerifyMsg.encode())

        sleep(0.1)
        with open(self._pro.FTPFilePath + filename, "wb") as f:
            while True:
                data = self.connfd.recv(1024)
                if data == self._pro.MsgFlag.encode():
                    return
                f.write(data)


class FTPServer:
    """
    FTP server
    """

    def __init__(self):
        self._sock = SocketModel()
        self._pro = ProtocalModel()
        self.list_client = []
        self.sockfd = socket()

    def create_socket(self):

        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self._sock.Server_ADDR)

        self.sockfd.listen(3)
        print("Listen the post %s ..." % self._sock.PORT)

    def tcp_server(self):
        """
        run server
        """
        self.create_socket()

        while True:
            try:
                connfd, addr = self.sockfd.accept()
                print("Connect from...", addr)
            except KeyboardInterrupt:
                sys.exit("Server Disconnect...")
            except Exception:
                print(Exception)
                continue

            t = FTPServerHandleRequest(connfd)
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    ftp = FTPServer()
    ftp.tcp_server()
