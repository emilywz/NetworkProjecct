"""
online dictionary client
evn:python3.6
"""
from socket import *
from model import *
import getpass, sys


class DictClientHandleRequest:
    def __init__(self, sockfd):
        self._pro = ProtocolModel()
        self._sock = SocketModel()
        self.sockfd = sockfd

    def ui_index_list(self):
        print()
        print("\n******** Welcome Page ********")
        print(" 1>Register  2>Login   3>Quit ")
        print("******************************")
        print()

    def ui_second_list(self):
        print()
        print("\n***********  Query Page  **********")
        print(" 1>LookupWord  2>History  3>Logoff ")
        print("***********************************")
        print()

    def register(self):
        """
        register function
        """
        while True:
            name = input("Register Name:")
            password = getpass.getpass()
            password_r = getpass.getpass("Confirm Password:")

            if password != password_r:
                print("Different Password,Please Reinput!")
                continue
            if (" " in name) or (" " in password):
                print("Please No Blank in Name or Password!")
                continue

            msg = self._pro.Register + " %s %s" % (name, password)
            self.sockfd.send(msg.encode())

            msg_server = self.sockfd.recv(128).decode()

            if msg_server == self._pro.VerifyMsg:
                print("Register Successfully")
                self.jump_page(name)
            else:
                print("Register Failed")
            return

    def login(self):
        """
        login function
        """
        name = input("Name:")
        password = getpass.getpass()

        msg = self._pro.Login + " %s %s" % (name, password)
        self.sockfd.send(msg.encode())

        msg_server = self.sockfd.recv(128).decode()

        if msg_server == self._pro.VerifyMsg:
            print("Login Successfully")
            self.jump_page(name)
        else:
            print("Login Failed")
        return

    def quit(self):
        """
        quit dict client
        """
        self.sockfd.send(self._pro.Quit.encode())
        self.sockfd.close()
        sys.exit("Thanks for Using Dict System,Bye Bye")

    def jump_second_page(self):
        while True:
            print("The Second Page")
            cmd = input(">")
            if cmd == '1':
                pass
            elif cmd == '2':
                break

    def jump_page(self, name):
        while True:
            self.ui_second_list()

            cmd = input("Input Your Choice:")

            if cmd.strip() == "1":
                self.lookup_word(name)
            elif cmd.strip() == "2":
                self.check_history(name)
            elif cmd.strip() == "3":
                return
            else:
                print("Please Input right command")
                continue

    def lookup_word(self, name):
        while True:
            word = input("Word As: ")
            if word == self._pro.MsgFlag:
                return
            msg = self._pro.LookupWord + " %s %s" % (name, word)
            self.sockfd.send(msg.encode())

            data = self.sockfd.recv(2048).decode()
            if data == self._pro.FailMsg:
                print("No such word as '%s' " % word)
                continue
            else:
                print("*****word explain as*****")
                print("%s : %s " % (word, data))
                print("*************************")


    def check_history(self,name):

        msg=self._pro.History+" "+name
        self.sockfd.send(msg.encode())

        data=self.sockfd.recv(128).decode()
        if data==self._pro.VerifyMsg:
            print("******** history as ********")
            while True:
                data = self.sockfd.recv(1024).decode()
                if data == self._pro.MsgFlag:
                    return
                print(data)
        else:
            print("No history")




class DictClient:
    """
    dict client
    """

    def __init__(self):
        self._sock = SocketModel()
        self.sockfd = socket()
        self._request = DictClientHandleRequest(self.sockfd)

    def __create_socket(self):
        try:
            self.sockfd.connect(self._sock.Server_ADDR)
        except Exception as e:
            print(e)
            return

    def tcp_client(self):
        """
        run client
        """
        self.__create_socket()

        while True:
            self._request.ui_index_list()

            cmd = input("Input Your Choice:")

            if cmd.strip() == "1":
                self._request.register()
            elif cmd.strip() == "2":
                self._request.login()
            elif cmd.strip() == "3":
                self._request.quit()
            else:
                print("Please Input right command")
                continue


if __name__ == '__main__':
    dict = DictClient()
    dict.tcp_client()
