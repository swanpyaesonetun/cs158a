# mychatclient.py
from socket import *
import threading

serverHost = "127.0.0.1"  # ip address (using local host)
serverPort = 12345  # port number

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

print("Connected to chat server. Type 'exit' to leave.")

# function to receive messages from the server
def receive():
    while True:
        try:
            message = clientSocket.recv(1024).decode() # receive and decode message
            if not message: # if message is empty, break loop
                break
            print("\n" + message) # print message
        except: # if error occurred, break loop
            break

# function to receive inputs and send to server
def write():
    while True:
        message = input()

        if message.lower() == "exit": # check exit condition
            clientSocket.send(message.encode())
            break
        try:
            clientSocket.send(message.encode())
        except: # if error occurred, break loop
            break

    print("Disconnected from server")
    clientSocket.close()
    exit()

# start the threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
