import socket
import threading

class BroadcastClient:
    def __init__(self, broadcast_address):
        self.broadcast_address = broadcast_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('', 37020))  # Bind to any address and a specific port

    def send_message(self, message):
        self.sock.sendto(message.encode('utf-8'), self.broadcast_address)

    def receive_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print(f'Received message: {data.decode("utf-8")} from {addr}')

    def start(self):
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

if __name__ == "__main__":
    broadcast_address = ('192.168.178.255', 37020)  # Replace with your chosen broadcast address and port

    client = BroadcastClient(broadcast_address)
    client.start()

    for _ in range(10):
        client.send_message("Hi wie gehts?")