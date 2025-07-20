import socket
import threading
import uuid
import json
import time


class Message:
    def __init__(self, uid, flag):
        self.uuid = str(uid)
        self.flag = flag

    def to_json(self):
        return json.dumps(self.__dict__) + "\n"

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        msg = Message(data['uuid'], data['flag'])
        return msg


def log_event(log_file, direction, msg, comparison=None, state=None):
    with open(log_file, 'a') as f:
        f.write(f"{direction}: uuid={msg.uuid}, flag={msg.flag}" +
                (f", {comparison}, {state}" if comparison else "") + "\n")


class Node:
    def __init__(self, config_path, log_path):
        self.uuid = uuid.uuid4()
        self.leader_id = None
        self.flag = 0  # 0: still electing, 1: leader elected
        self.config_path = config_path
        self.log_path = log_path
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.neighbor_socket = None

        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            lines = f.readlines()
            self.my_ip, self.my_port = lines[0].strip().split(',')
            self.neighbor_ip, self.neighbor_port = lines[1].strip().split(',')
            self.my_port = int(self.my_port)
            self.neighbor_port = int(self.neighbor_port)

    def start_server(self):
        self.server_socket.bind((self.my_ip, self.my_port))
        self.server_socket.listen(1)
        self.neighbor_socket, _ = self.server_socket.accept()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def start_client(self):
        while True:
            try:
                self.client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(
                    (self.neighbor_ip, self.neighbor_port))
                break
            except:
                time.sleep(1)

        # Send initial message
        msg = Message(self.uuid, 0)
        self.send_message(msg)

    def send_message(self, msg):
        log_event(self.log_path, "Sent", msg)
        self.client_socket.sendall(msg.to_json().encode())

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
        comparison = "greater" if msg.uuid > str(
            self.uuid) else "less" if msg.uuid < str(self.uuid) else "same"
        log_event(self.log_path, "Received", msg, comparison, self.flag)

        if msg.flag == 1:
            self.leader_id = msg.uuid
            self.flag = 1
            if self.leader_id == str(self.uuid):
                print(f"leader is {self.leader_id}")
            else:
                self.send_message(msg)
            return

        if msg.uuid == str(self.uuid):
            self.flag = 1
            self.leader_id = str(self.uuid)
            print(f"leader is {self.leader_id}")
            new_msg = Message(self.uuid, 1)
            self.send_message(new_msg)
        elif msg.uuid > str(self.uuid):
            self.send_message(msg)
        else:
            with open(self.log_path, 'a') as f:
                f.write("Ignored message\n")

    def run(self):
        threading.Thread(target=self.start_server, daemon=True).start()
        time.sleep(2)
        self.start_client()

        # Keep main thread alive
        while True:
            time.sleep(1)


if __name__ == "__main__":
    import sys
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    log_file = sys.argv[2] if len(sys.argv) > 2 else "log.txt"
    node = Node(config_file, log_file)
    node.run()
