# myvlserver.py
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive...")

def receive_full_message(conn, msg_len):
    data = b''
    while len(data) < msg_len:
        chunk = conn.recv(min(64, msg_len - len(data)))
        if not chunk:
            break
        data += chunk
    return data.decode()


while True:
    cnSocket, addr = serverSocket.accept()
    print(f'Connected from {addr[0]}')

    # Step 1: Read 2-byte message length header
    length_header = cnSocket.recv(2)
    if not length_header:
        cnSocket.close()
        continue

    msg_len = int(length_header.decode())
    print(f'msg_len: {msg_len}')

    # Step 2: Read actual message content
    sentence = receive_full_message(cnSocket, msg_len)
    print(f'processed: {sentence}')

    # Step 3: Process and send back
    capSentence = sentence.upper()
    cnSocket.send(capSentence.encode())

    print(f'msg_len_sent: {len(capSentence)}')
    cnSocket.close()
    print('Connection closed\n')
