# mychatclient.py
from socket import *
import threading

serverHost = "127.0.0.1"  # ip address
serverPort = 12345  # port number

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

print("Connected to chat server. Type 'exit' to leave.")


def receive():
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            break


def write():
    while True:
        message = input()

        if message.lower() == "exit":
            clientSocket.send(message.encode())
            break
        try:
            clientSocket.send(message.encode())
        except:
            break

    print("Disconnected from server")
    clientSocket.close()
    exit()


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
