from client import Client
import time

c1 = Client("Guy")
c2 = Client("Unknown")

c1.send_message("hello")
time.sleep(1)
c2.send_message("Whats up")
time.sleep(1)
c1.send_message("nothing much, hbu")
time.sleep(1)
c2.send_message("Boring...")

c1.disconnect()
time.sleep(2)
c2.disconnect()

def update_message():
    time.sleep(2)