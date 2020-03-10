"""
ftp 文件传输客户端
"""

from socket import *
from model import *
from time import *
import sys


class FTPClientHandleRequest:
    """
    客户端查看文件列表,下载,上传,退出
    """

    def __init__(self, sockfd):
        self._pro = ProtocalModel()
        self.sockfd = sockfd

    def choose_ui_list(self):
        """
        选择界面
        """
        print("\n=====File Command=====")
        print("******** list ********")
        print("****** download ******")
        print("******* upload *******")
        print("******** quit ********")
        print("======================")

    def check_list(self):
        """
        查看文件列表
        """
        # 发送请求
        self.sockfd.send(self._pro.FileList.encode())
        # 等待服务端回复
        data = self.sockfd.recv(128).decode()
        if data == self._pro.VerifyMsg:
            # 一次接收所有文件名
            filelist = self.sockfd.recv(4096)
            print(filelist.decode())
        else:
            print(data)

    def download_file(self, filename):
        """
        下载文件
        :param filename: 目标文件名
        """
        self.sockfd.send((self._pro.DownloadFile + " " + filename).encode())

        data = self.sockfd.recv(128).decode()

        if data == self._pro.VerifyMsg:
            f = open(filename, "wb+")
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == self._pro.MsgFlag:
                    break
                f.write(data)

            f.close()

    def upload_file(self, filename):
        """
        上传文件
        :param filename: 文件名(可以是完整路径的文件)
        """
        try:
            f = open(filename, "rb")
        except Exception:
            print("File not exist")
            return

        filename = filename.split("/")[-1]
        self.sockfd.send((self._pro.UploadFile + " " + filename).encode())

        data = self.sockfd.recv(128).decode()
        if data == self._pro.VerifyMsg:
            with open(filename, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        sleep(0.1)
                        self.sockfd.send(self._pro.MsgFlag)
                        return
                    self.sockfd.send(data)

    def quit(self):
        """
        退出TFP传输服务
        :return:
        """
        self.sockfd.send(self._pro.Quit.encode())
        self.sockfd.close()
        sys.exit("Thanks for Using FTP System")


class FTPClient:
    """
    客户端连接
    """

    def __init__(self):
        self._sock = SocketModel()
        self._pro = ProtocalModel()
        self.sockfd = socket()
        self.request = FTPClientHandleRequest(self.sockfd)

    def create_socket(self):
        """
        创建套接字
        """
        try:
            self.sockfd.connect(self._sock.Server_ADDR)
        except Exception:
            print(Exception)
            return

    def tcp_client(self):
        """
        客户端运行
        """
        self.create_socket()

        while True:
            self.request.choose_ui_list()

            cmd = input("Input Your Choice:")

            if not cmd:
                break
            elif cmd.strip() == "list":
                self.request.check_list()
            elif cmd.strip() == "quit":
                self.request.quit()
            elif cmd.strip().split(" ")[0] == "download":
                filename = cmd.strip().split(" ")[-1]
                self.request.download_file(filename)
            elif cmd.strip().split(" ")[0] == "upload":
                filename = cmd.strip().split(" ")[-1]
                self.request.upload_file(filename)
            else:
                print("Please Input right command")

            self.sockfd.send(cmd.encode())
            data = self.sockfd.recv(1024)
            print("Receive Msg from server:", data.decode())


if __name__ == '__main__':
    tcp = FTPClient()
    tcp.tcp_client()
