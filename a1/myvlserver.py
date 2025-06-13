from socket import *

serverPort = 12000  # Port number

serverSocket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket

# This empty string means the server will listen on all available interfaces
serverSocket.bind(('', serverPort))  # Bind the socket to the port

serverSocket.listen(1)  # Listen for incoming connections

while True:
    # Accept
    cnSocket, addr = serverSocket.accept()  # Accept a connection from a client
    # Print the address of the connected client
    print(f'Connection from {addr}')

    # Receive
    sentence = cnSocket.recv(64).decode()  # Receive a sentence from the client

    length = int(sentence[:2])
    message = sentence[2:]

    # Process
    sent_length = 0
    i = 0
    capSentence = ""
    # Convert the sentence to uppercase
    while sent_length < length:
        capSentence += message[i].upper()
        sent_length += 1
        i += 1

    # Send
    # Send the modified sentence back to the client
    cnSocket.send(capSentence.encode())

    print("msg_len: ", length)
    print("processed: ", message)
    print("msg_len_sent: ", sent_length)

    # Close
    cnSocket.close()  # Close the connection with the client
    print("Connection closed")
