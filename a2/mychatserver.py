# myvlserver.py
from socket import *
import threading

serverHost = "127.0.0.1"  # ip address
serverPort = 12345  # port number

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen()

print(f"Server listening on {serverHost}:{serverPort}")

clients = []


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message.encode())


def handle(client, addr):
    while True:
        try:
            message = client.recv(1024).decode()
            if message.lower() == "exit":
                break
            formatted = f"{addr[1]}: {message}"
            print(formatted)
            broadcast(formatted, client)
        except:
            break

    print(f"Client {addr[1]} disconnected")
    clients.remove(client)
    client.close()


def receive():
    while True:
        client, addr = serverSocket.accept()
        print(f"New connection from {addr}")
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client, addr))
        thread.start()


receive()
