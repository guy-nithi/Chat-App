from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

from person import Person

# Global variable
HOST = 'localhost'
# HOST = '' # Hong
PORT = 8080
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# Local variable
persons = []


def broadcast(msg, name):
    # print("I'm in broadcast.") # Hong
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[EXCEPTION", e)
        # client.send(bytes(name + ": ", "utf8") + msg) # Hong


def client_communication(person):
    # print("I'm in client_communication.") # Hong
    client = person.client

    # First message received is always the person name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # Broadcast welcome message

    while True:  # Wait for any message from
        msg = client.recv(BUFSIZ)

        if msg == bytes("{quit}", "utf8"):  # If message is quit disconnect client
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
            print(f"[DISCONNECTED] {name} disconnected")
            break
        else:  # Otherwise, send message to all others clients
            broadcast(msg, name + ": ")
            print(f"{name}: ", msg.decode("utf8"))


def wait_for_connection():
    # print("I'm in wait_for_connection.") # Hong

    while True:
        try:
            client, addr = SERVER.accept()  # Wait for any new connections
            person = Person(addr, client)  # Create new person for connection
            persons.append(person)

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()  # GUY! You're missing ()!
        except Exception as e:
            print("[EXCEPTION]", e)
            break

    print("SERVER CRASHED")


if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS)  # Open server to listen for connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    print(ACCEPT_THREAD)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
