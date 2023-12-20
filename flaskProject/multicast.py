import socket
import struct
import threading

class MulticastClient:
    def __init__(self, multicast_group, server_address):
        self.multicast_group = multicast_group
        self.server_address = server_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.2)

        # Join the multicast group
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def send_message(self, message):
        self.sock.sendto(message.encode('utf-8'), self.server_address)

    def receive_messages(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
                print(f'Received message: {data.decode("utf-8")}')
            except socket.timeout:
                continue

    def start(self):
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

if __name__ == "__main__":
    multicast_group = '224.0.0.100'  # Replace with your chosen multicast group
    server_address = (multicast_group, 10000)  # Replace 10000 with your chosen port number

    client = MulticastClient(multicast_group, server_address)
    client.start()

    while True:
        message = input("Enter message to send (press Enter to stop): ")
        if message == "":
            break
        client.send_message(message)