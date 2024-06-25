import socket
from threading import Thread

def recvMessage(sock):
    while True:
        msg = sock.recv(1024)
        print(msg.decode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9826))

th = Thread(target = recvMessage, args = (sock, ))
th.daemon = True
th.start()

first_state = True

while True:
    msg = input()
    sock.send(msg.encode())
    if msg == "/exit":
        break

sock.close()