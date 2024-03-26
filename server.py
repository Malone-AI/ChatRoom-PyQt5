import time
import socket
import threading

class Server(object):
    def __init__(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(("192.168.222.1",9999))
        self.server.listen(5)
        # 所有客户端
        self.clients = []
        # 用户名及ip的字典
        self.clients_name_ip = {}

        self.get_connection()
    
    def get_connection(self):
        # 监听客户端连接
        while True:
            client,address = self.server.accept()
            print(address)
            data = "成功连接到服务器！请输入你的昵称:"
            client.send(data.encode())
            self.clients.append(client)
            threading.Thread(target = self.get_msg,args = (client,address)).start()
    
    def get_msg(self,client,address):
        name = client.recv(1024).decode()
        self.clients_name_ip[address] = name

        while True:
            # 获取所有客户端发的消息
            try:
                recv_data = client.recv(1024).decode()
            except Exception as e:
                self.close_client(client,address)
                break
            # 用户输入"Q"退出
            if recv_data.upper() == "Q":
                self.close_client(client,address)
                break
            for c in self.clients:
                c.send((self.clients_name_ip[address] + " " + 
                       time.strftime("%Y-%m-%d %H-%M-%S",time.localtime()) + "\n" + recv_data).encode())

    def close_client(self,client,address):
        self.clients.remove(client)
        client.close()
        notice = str(self.clients_name_ip[address]) + "已经离开"
        print(notice)
        for c in self.clients:
            c.send(notice.encode())

if __name__ == "__main__":
    print("服务器正在运行在......")
    Server()