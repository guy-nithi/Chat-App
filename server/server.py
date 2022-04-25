from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from person import Person

# global variable
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# local variable
persons = []

def broadcast(msg, name):
    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf8"))

def client_communication(person):
    client = person.client
    addr = person.addr

    # Get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    msg = bytes(f"{name} has joined the chat!")
    broadcast(msg,name) # Broadcast welcome message

    while True:
        try:
            msg = client.recv(BUFSIZ)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes("{quit}", "utf8"):
                broadcast(f"{name} has left the chat...", "")
                client.send(bytes("{quit}", "utf8"))
                client.close()

                persons.remove(person)
                break
            else:
                broadcast(msg, name)
        except Exception as e:
            print("[EXCEPTION]", e)
            break

def wait_for_connection():
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False

    print("SERVER CRASHED")

if __name__ == '__main__':
    SERVER.listen(10) # Listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()