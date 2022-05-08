from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock

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
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        messages_copy = self.messages[:]
        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy

    def disconnect(self):
        self.send_message(bytes("{quit}", "utf8"))
