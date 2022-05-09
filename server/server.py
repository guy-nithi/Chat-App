from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from person import Person

# global variable
HOST = 'localhost'
# HOST = '' # Hong
PORT = 8080
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# local variable
persons = []

def broadcast(msg, name):
    # print("I'm in broadcast.") # Hong
    for person in persons:
        client = person.client
        client.send(bytes(name + ": ", "utf8"))
        # client.send(bytes(name + ": ", "utf8") + msg) # Hong

def client_communication(person):
    # print("I'm in client_communication.") # Hong
    client = person.client
    addr = person.addr

    # Get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    # person.set_name(name) # Hong
    msg = bytes(f"{name} has joined the chat!", "utf8") # GUY! You're missing "utf8"!
    person.set_name(name)
    broadcast(msg, "") # Broadcast welcome message
    # broadcast(msg, "") # Hong

    while True:
        try:
            msg = client.recv(BUFSIZ)

            if msg == bytes("{quit}", "utf8"):
                client.send(bytes("{quit}", "utf8"))
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                broadcast(msg, name+": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXCEPTION]", e)
            break

def wait_for_connection():
    # print("I'm in wait_for_connection.") # Hong
    run = True

    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start() # GUY! You're missing ()!
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False

    print("SERVER CRASHED")

if __name__ == '__main__':
    SERVER.listen(10) # Listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    print(ACCEPT_THREAD)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()