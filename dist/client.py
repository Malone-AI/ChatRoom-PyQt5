import sys
import socket
import threading
import rec
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt5.QtCore import *


class Client(object):
    def __init__(self):
        self.ui = uic.loadUi("chat.ui")
        self.ui.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.setAttribute(Qt.WA_TranslucentBackground)
        self.add_ui()
        # 与服务器连接
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(("192.168.222.1",9999))
        self.button.clicked.connect(self.send_msg)
        self.work_thread()
    
    def add_ui(self):
        self.content = self.ui.textBrowser
        self.message = self.ui.lineEdit
        self.button = self.ui.pushButton
    
    def send_msg(self):
        msg = self.message.text()
        self.client.send(msg.encode())
        if msg.upper() == "Q":
            self.client.close()
            self.destroy()
        self.message.clear()

    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                print(data)
                data = data + "\n"
                self.content.append(data)
            except:
                exit()
    
    def work_thread(self):
        # 线程处理
        threading.Thread(target = self.send_msg).start()
        threading.Thread(target = self.recv_msg).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Client().ui
    win.show()
    app.exec_()