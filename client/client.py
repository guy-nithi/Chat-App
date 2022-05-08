from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock
import threading
import time

class Client:
    HOST = '' # Hong
    HOST = 'localhost'
    PORT = 8080
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        self.receive_thread = Thread(target=self.receive_message)
        self.receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receive_message(self):
        while True:
            try:
                msg = self.client_socket.recv(self. BUFSIZ).decode()
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
                print(msg)
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_message(self,msg):
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        self.lock.acquire()
        self.lock.release()
        return self.messages

    def disconnect(self):
        self.send_message("{quit}")
