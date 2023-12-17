import socket
import threading
import time
import uuid
import struct
from datetime import datetime

class Network:
    clients_network = []
    replication_network = ['192.168.0.1', '130.234.204.2', '130.234.203.2', '130.234.204.1', '182.4.3.111']
    replication_network_ring = []
    clients_network_ring = []

    def __init__(self):
        self.ring = self.replication_network  # assuming replication_network as the ring

    def add_host(self, host):
        if host not in self.replication_network:
            self.replication_network.append(host)
        else:
            print(f"Host {host} was already discovered")

    def remove_host(self, host):
        if host in self.replication_network:
            self.replication_network.remove(host)
        else:
            print(f"Host {host} was already removed")

    def add_client(self, host):
        if host not in self.clients_network:
            self.clients_network.append(host)
        else:
            print(f"Client {host} was already added")

    def remove_client(self, client):
        if client in self.clients_network:
            self.clients_network.remove(client)
        else:
            print(f"Host {client} was already removed")

    def get_hosts(self):
        return self.replication_network

    def get_client(self):
        return self.clients_network

    @staticmethod
    def form_ring(replication_network):
        sorted_binary_ring = sorted([socket.inet_aton(replication_network) for replication_network in replication_network])
        print('Sorted Binary')
        print(sorted_binary_ring)
        sorted_ip_ring = [socket.inet_ntoa(node) for node in sorted_binary_ring]
        print('Sorted IP')
        print(sorted_ip_ring)
        return sorted_ip_ring

    @staticmethod
    def get_neighbour(ring, current_node_ip, direction="right"):
        current_node_index = ring.index(current_node_ip) if current_node_ip in ring else -1
        if current_node_index != -1:
            if direction == 'right':
                if current_node_index + 1 == len(ring):
                    return ring[0]
                else:
                    return ring[current_node_index + 1]
            else:
                if current_node_index == 0:
                    return ring[len(ring) - 1]
                else:
                    return ring[current_node_index - 1]
        else:
            return None

    @staticmethod
    def get_ownip():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        return ip_address

    @staticmethod
    def get_time():
        timest = time.time()
        date_time = datetime.fromtimestamp(timest)
        print(date_time.strftime("%Y-%m-%d %H:%M:%S"))
        return timest

    @staticmethod
    def send_heartbeat():
        while True:
            MCAST_GRP = '224.1.1.1'
            MCAST_PORT = 5007

            heartbeat_message = {
                "id": str(uuid.uuid4()),
                "sender": Network.get_ownip(),
                "timestamp": Network.get_time(),
            }

            heartbeat_msg = f"HB:{heartbeat_message['id']}:{heartbeat_message['sender']}"
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            sock.sendto(heartbeat_msg.encode(), (MCAST_GRP, MCAST_PORT))
            print(heartbeat_msg)

            # Warte für 3 Sekunden, bevor die nächste Herzschlagnachricht gesendet wird
            time.sleep(3)

    def start_sending_heartbeat(self):
        # Erstelle einen Thread für die Methode send_heartbeat
        sender_thread = threading.Thread(target=self.send_heartbeat)
        # Setze den Thread als Hintergrundthread, damit er beendet wird, wenn das Hauptprogramm beendet wird
        sender_thread.daemon = True
        # Starte den Thread
        sender_thread.start()

    @staticmethod
    def receive_heartbeat():
        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            message = sock.recv(10240)
            # Hier kannst du die empfangene Nachricht verarbeiten oder entsprechend reagieren
            print(f"Received message: {message.decode('utf-8')}")

    def start_listening(self):
        # Erstelle einen Thread für die Methode receive_heartbeat
        listener_thread = threading.Thread(target=self.receive_heartbeat)
        # Setze den Thread als Hintergrundthread, damit er beendet wird, wenn das Hauptprogramm beendet wird
        listener_thread.daemon = True
        # Starte den Thread
        listener_thread.start()


if __name__ == '__main__':
    network_instance = Network()
    network_instance.send_heartbeat()
    own_ip = network_instance.get_ownip()
    network_instance.add_client(own_ip)
    network_instance.add_host(own_ip)
    print(network_instance.clients_network)
    print(network_instance.replication_network)
    print(network_instance.get_neighbour(network_instance.ring, str(own_ip), "left"))
