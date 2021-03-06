from client import Client
import time
from threading import Thread

c1 = Client("Guy")
c2 = Client("Unknown")


def update_message():
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # Update every 1/10 of a second
        new_messages = c1.get_messages()  # Get any new messages from client
        msgs.extend(c1.get_messages())  # Add to local list of messages

        for msg in new_messages:  # Display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_message).start()

c1.send_message("hello")
time.sleep(1)
c2.send_message("Whats up")
time.sleep(1)
c1.send_message("nothing much, hbu")
time.sleep(1)
c2.send_message("Bruh why u asking dude...")

c1.disconnect()
time.sleep(2)
c2.disconnect()