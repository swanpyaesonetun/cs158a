import socket
import threading
import uuid
import json
import time

class Message:
    def __init__(self, uuid_str, flag):
        self.uuid = uuid_str
        self.flag = flag

    def to_json(self):
        return json.dumps(self.__dict__) + "\n"

    @staticmethod
    def from_json(data):
        obj = json.loads(data)
        return Message(obj['uuid'], obj['flag'])

class Node:
    def __init__(self, config_file, log_file):
        self.uuid = str(uuid.uuid4())
        self.leader_id = None
        self.state = 0  # 0: electing, 1: elected
        self.log_file = log_file
        self.server_socket = None
        self.client_socket = None
        self.neighbor_socket = None
        self.forwarded_leader = False


        with open(config_file, 'r') as f:
            lines = f.read().splitlines()
            self.my_ip, self.my_port = lines[0].split(',')
            self.peer_ip, self.peer_port = lines[1].split(',')
            self.my_port = int(self.my_port)
            self.peer_port = int(self.peer_port)

    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + "\n")
        print(message)

    def start_server(self):
        def server_thread():
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.my_ip, self.my_port))
            self.server_socket.listen(1)
            self.neighbor_socket, _ = self.server_socket.accept()
            self.receive_messages()

        threading.Thread(target=server_thread, daemon=True).start()

    def start_client(self):
        while True:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.peer_ip, self.peer_port))
                break
            except:
                time.sleep(1)

        # send initial message
        msg = Message(self.uuid, 0)
        self.send_message(msg)

    def send_message(self, msg):
        while self.client_socket is None:
            time.sleep(0.5)  # Wait for connection to be established
        self.client_socket.sendall(msg.to_json().encode())
        self.log(f"Sent: uuid={msg.uuid}, flag={msg.flag}")

    def receive_messages(self):
        buffer = ""
        while True:
            data = self.neighbor_socket.recv(1024).decode()
            if not data:
                break
            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                msg = Message.from_json(line)
                self.handle_message(msg)

    def handle_message(self, msg):
        comparison = "same" if msg.uuid == self.uuid else ("greater" if msg.uuid > self.uuid else "less")

        if msg.flag == 1:
            self.state = 1
            self.leader_id = msg.uuid
            self.log(f"Received: uuid={msg.uuid}, flag=1, {comparison}, 1")

            if not self.forwarded_leader:
                self.send_message(msg)
                self.forwarded_leader = True
            elif msg.uuid == self.uuid:
                self.log("Termination condition met. Stopping forwarding.")
            return

        if self.state == 1:
            self.log(f"Ignored message from uuid={msg.uuid} as already elected")
            return

        self.log(f"Received: uuid={msg.uuid}, flag=0, {comparison}, 0")

        if msg.uuid > self.uuid:
            self.send_message(msg)
        elif msg.uuid == self.uuid:
            self.state = 1
            self.leader_id = self.uuid
            self.log(f"Leader is decided to {self.leader_id}.")
            new_msg = Message(self.uuid, 1)
            self.send_message(new_msg)
        # else: don't forward smaller UUIDs

    def run(self):
        self.start_server()
        time.sleep(2)  # wait for servers to be ready
        self.start_client()

        while self.state == 0:
            time.sleep(1)
        self.log(f"Final Leader: {self.leader_id}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python myleprocess.py <config.txt> <log.txt>")
        exit(1)

    node = Node(sys.argv[1], sys.argv[2])
    node.run()
