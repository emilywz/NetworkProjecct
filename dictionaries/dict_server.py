"""
dictionary online server
evn:python3.6
"""
from model import *
from dict_database import *
from socket import *
from threading import Thread
from time import sleep
import sys



class DictServerHandleRequest(Thread):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd
        self._sock=SocketModel()
        self._pro = ProtocolModel()
        self._db=DictDataBaseModel(database="dict")

    def run(self):
        self._db.create_cur()
        while True:
            data = self.connfd.recv(1024).decode()
            temp = data.strip().split(" ")
            if not data or temp[0]==self._pro.Quit:
                return
            elif temp[0] == self._pro.Register:
                self.register(temp[1],temp[2])
            elif temp[0]==self._pro.Login:
                self.login(temp[1],temp[2])

            elif temp[0]==self._pro.LookupWord:
                self.query_dict(temp[1],temp[2])
            elif temp[0]==self._pro.History:
                self.check_history(temp[1])


    def register(self,name,password):
        if self._db.handle_register_data(name,password):
            self.connfd.send(self._pro.VerifyMsg.encode())
        else:
            self.connfd.send(self._pro.FailMsg.encode())


    def login(self,name,password):
        if self._db.handle_login_data(name, password):
            self.connfd.send(self._pro.VerifyMsg.encode())
        else:
            self.connfd.send(self._pro.FailMsg.encode())


    def query_dict(self,name,word):
        self._db.add_history_word(name,word)
        meaning=self._db.handle_query_dict(word)
        if meaning:
            self.connfd.send(meaning.encode())
        else:
            self.connfd.send(self._pro.FailMsg.encode())


    def check_history(self,name):
        history=self._db.handle_check_history(name)
        if history:
            self.connfd.send(self._pro.VerifyMsg.encode())
            for note in history:
                sleep(0.1)
                info="%s %-16s %s"%note
                self.connfd.send(info.encode())

            sleep(0.1)
            self.connfd.send(self._pro.MsgFlag.encode())
        else:
            self.connfd.send(self._pro.FailMsg.encode())


class DictServer:
    def __init__(self):
        self._sock = SocketModel()
        self.__create_socket()

    def __create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self._sock.Server_ADDR)
        self.sockfd.listen(3)
        print("Listen the port %s..." % self._sock.PORT)

    def tcp_server(self):
        """
        run tcp server
        """
        while True:
            try:
                connfd, addr = self.sockfd.accept()
                print("Connect from...", addr)
            except KeyboardInterrupt:
                sys.exit("Server Disconnect...")
            except Exception as e:
                print(e)
                continue

            t = DictServerHandleRequest(connfd)
            t.setDaemon(True)
            t.start()

if __name__ == '__main__':
    dict=DictServer()
    dict.tcp_server()
