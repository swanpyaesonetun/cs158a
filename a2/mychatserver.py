# myvlserver.py
from socket import *
import threading

serverHost = "127.0.0.1"  # ip address (using local host)
serverPort = 12345  # port number

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverHost, serverPort))
serverSocket.listen()

print(f"Server listening on {serverHost}:{serverPort}")

clients = [] # list to store connected clients

# function to broadcast messages to all clients except sender
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message.encode())

# function to receive messages from the client
def handle(client, addr):
    while True:
        try:
            message = client.recv(1024).decode()
            if message.lower() == "exit": # check exit condition
                break
            formatted = f"{addr[1]}: {message}" # format the message
            print(formatted) # display message on server side
            broadcast(formatted, client) # broadcast message to all clients
        except: # if error occurred, break loop
            break

    print(f"Client {addr[1]} disconnected")
    clients.remove(client) # remove client from connected clients list
    client.close()

# function to accept client connections
def receive():
    while True:
        client, addr = serverSocket.accept() # accept connection
        print(f"New connection from {addr}")
        clients.append(client) # add client to connected clients list

        thread = threading.Thread(target=handle, args=(client, addr)) # start receiving message from client
        thread.start()


receive()
