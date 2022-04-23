from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from server.person import Person

# global variable
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
BUFSIZ = 512

# local variable
persons = {}

def broadcast():
    pass

def client_communication(person):
    client = person.client
    addr = person.addr

    # Get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    msg = f"{name} has joined the chat!"
    broadcast(msg)

    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("{quit}", "utf8"):
            client.close()
        else:
            pass

def wait_for_connection():
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start
        except Exception as e:
            print("[FAILURE]", e)
            run = False

    print("SERVER CRASHED")

if __name__ == '__main__':
    SERVER.listen(10) # Listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()