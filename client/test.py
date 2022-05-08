from client import client
import time

c1 = client()
c2 = client()

c1.send_message("hello")
c2.send_message("Whats up")
time.sleep(1)
c1.send_message("nothing much, hbu")
time.sleep(1)
c2.send_message("Boring...")