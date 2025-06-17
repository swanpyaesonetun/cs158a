# myvlclient.py
from socket import *

serverName = '10.1.10.154'  # localhost or actual server IP
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Input includes length + message (e.g. "10helloworld")
sentence = input('Input lowercase sentence: ')

# Input validation
if len(sentence) < 3 or len(sentence) > 101:
    print("Input must include a 2-digit length prefix and at least 1 character.")
    clientSocket.close()
    exit()

try:
    msg_len = int(sentence[:2])
except ValueError:
    print("First two characters must be a number (01-99).")
    clientSocket.close()
    exit()

message = sentence[2:]

# Validate declared length vs actual
if msg_len < 1 or msg_len > 99 or len(message) != msg_len:
    print(
        f"Declared length = {msg_len}, actual length = {len(message)}. They must match and be between 1–99.")
    clientSocket.close()
    exit()

# Send the first 2 bytes = length, then the message
clientSocket.send(sentence[:2].encode())  # length header
clientSocket.send(message.encode())       # message body

# Receive and print result
modifiedSentence = b''
while True:
    chunk = clientSocket.recv(64)
    if not chunk:
        break
    modifiedSentence += chunk

print('From Server:', modifiedSentence.decode())
clientSocket.close()
