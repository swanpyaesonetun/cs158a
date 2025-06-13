from socket import *

serverName = '10.0.0.215'  # ip address
serverPort = 12000  # port number

# TCP SOCKET_STREAM
clientSocket = socket(AF_INET, SOCK_STREAM)
# Connect to the server
clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence: ')

length = sentence[:2]
message = sentence[2:]

clientSocket.send(sentence.encode())  # Send the sentence to the server

# Receive the modified sentence from the server
modifiedSentence = clientSocket.recv(64)

print('From Server: ', modifiedSentence.decode())
