from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import time

# GLOBAL CONSTANTS
HOST = '' # Hong
HOST = 'localhost'
PORT = 8080
ADDR = (HOST, PORT)
BUFSIZ = 512

# GLOBAL VARIABLES
messages = []

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

def receive_message():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode()
            messages.append(msg)
            print(msg)
        except Exception as e:
            print("[EXCEPTION]", e)
            break

def send_message(msg):
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()


receive_thread = Thread(target=receive_message)
receive_thread.start()

send_message("Guy")
time.sleep(10)
send_message("Hello By User: Guy")
send_message(f"{quit}")