import socket
import threading
import time
import uuid
from datetime import datetime
import multicast

class Network:
    """
    Represents a network of hosts and clients.

    Attributes:
    - clients_network (list): List of clients in the network.
    - replication_network (list): List of replication servers in the network.
    - replication_network_ring (list): List of replication servers arranged in a ring.
    - clients_network_ring (list): List of clients arranged in a ring.
    - ring (list): The current ring being used for replication.

    Methods:
    - __init__(): Initializes the Network object.
    - add_host(host): Adds a host to the replication network.
    - remove_host(host): Removes a host from the replication network.
    - add_client(host): Adds a client to the network.
    - remove_client(client): Removes a client from the network.
    - get_hosts(): Returns the replication network.
    - get_client(): Returns the clients network.
    - form_ring(replication_network): Forms a ring from the replication network.
    - get_neighbour(ring, current_node_ip, direction): Returns the neighbour of a node in the ring.
    - get_ownip(): Returns the IP address of the current device.
    - get_network_ip(): Returns the network IP address of the current device.
    - get_time(): Returns the current timestamp.
    - send_and_receive_heartbeat(): Sends and receives heartbeat messages.
    - receive_messages(): Receives messages from the network.
    - check_heartbeats(): Checks the heartbeats of the hosts in the network.
    """
    clients_network = []
    replication_network = ['192.168.0.1', '130.234.204.2', '130.234.203.2', '130.234.204.1', '182.4.3.111']
    replication_network_ring = []
    clients_network_ring = []

    def __init__(self):
        """
        Initializes the Network object.
        - Sets the replication network as the ring.
        - Starts a thread to check heartbeats.
        """
        self.ring = self.replication_network  # assuming replication_network as the ring
        self.last_heartbeat = {}  # Stores the last heartbeat timestamp from each server
        threading.Thread(target=self.check_heartbeats).start()

    def add_host(self, host):
        """
        Adds a host to the replication network.

        Parameters:
        - host (str): The host to be added.

        Returns:
        None
        """
        if host not in self.replication_network:
            self.replication_network.append(host)
        else:
            print(f"Host {host} was already discovered")

    def remove_host(self, host):
        """
        Removes a host from the replication network.

        Parameters:
        - host (str): The host to be removed.

        Returns:
        None
        """
        if host in self.replication_network:
            self.replication_network.remove(host)
        else:
            print(f"Host {host} was already removed")

    def add_client(self, host):
        """
        Adds a client to the network.

        Parameters:
        - host (str): The client to be added.

        Returns:
        None
        """
        if host not in self.clients_network:
            self.clients_network.append(host)
        else:
            print(f"Client {host} was already added")

    def remove_client(self, client):
        """
        Removes a client from the network.

        Parameters:
        - client (str): The client to be removed.

        Returns:
        None
        """
        if client in self.clients_network:
            self.clients_network.remove(client)
        else:
            print(f"Host {client} was already removed")

    def get_hosts(self):
        """
        Returns the replication network.

        Returns:
        list: The replication network.
        """
        return self.replication_network

    def get_client(self):
        """
        Returns the clients network.

        Returns:
        list: The clients network.
        """
        return self.clients_network

    @staticmethod
    def form_ring(replication_network):
        """
        Forms a ring from the replication network.

        Parameters:
        - replication_network (list): The replication network.

        Returns:
        list: The replication network arranged in a ring.
        """
        sorted_binary_ring = sorted([socket.inet_aton(replication_network) for replication_network in replication_network])
        print('Sorted Binary')
        print(sorted_binary_ring)
        sorted_ip_ring = [socket.inet_ntoa(node) for node in sorted_binary_ring]
        print('Sorted IP')
        print(sorted_ip_ring)
        return sorted_ip_ring

    @staticmethod
    def get_neighbour(ring, current_node_ip, direction="right"):
        """
        Returns the neighbour of a node in the ring.

        Parameters:
        - ring (list): The ring.
        - current_node_ip (str): The IP address of the current node.
        - direction (str): The direction to find the neighbour. Defaults to "right".

        Returns:
        str: The IP address of the neighbour.
        """
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
        """
        Returns the IP address of the current device.

        Returns:
        str: The IP address of the current device.
        """
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")
        return ip_address

    @staticmethod
    def get_network_ip():
        """
        Returns the network IP address of the current device.

        Returns:
        str: The network IP address of the current device.
        """
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[-1]
        ips = [ip for ip in ip_addresses if not ip.startswith('127.') and not ip.startswith('::1')]
        if ips:
            return ips[0]
        return "Keine IP-Adresse gefunden"

    @staticmethod
    def get_time():
        """
        Returns the current timestamp.

        Returns:
        float: The current timestamp.
        """
        timest = time.time()
        date_time = datetime.fromtimestamp(timest)
        print(date_time.strftime("%Y-%m-%d %H:%M:%S"))
        return timest

    @staticmethod
    def send_and_receive_heartbeat():
        """
        Sends and receives heartbeat messages.

        Returns:
        None
        """
        multicast_group = '224.0.0.100'  # Replace with your chosen multicast group
        server_address = (multicast_group, 10000)  # Replace 10000 with your chosen port number

        server = multicast.MulticastClient(multicast_group, server_address)
        server.start()

        heartbeat_message = {
            "id": str(uuid.uuid4()),
            "sender": Network.get_ownip(),
            "timestamp": Network.get_time(),
        }
        heartbeat_msg = f"HB:{heartbeat_message['id']}:{heartbeat_message['sender']}"
        server.send_message(heartbeat_msg)
        received_message = server.receive_messages()

    def receive_messages(self):
        """
        Receives messages from the network.

        Returns:
        None
        """
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                print(f'Received message: {data.decode("utf-8")} from {addr}')

                message_parts = data.decode("utf-8").split(':')
                if message_parts[0] == 'HB':
                    self.last_heartbeat[addr] = time.time()

            except socket.timeout:
                continue

    def check_heartbeats(self):
        """
        Checks the heartbeats of the hosts in the network.

        Returns:
        None
        """
        while True:
            time.sleep(1)
            for host in list(self.last_heartbeat.keys()):
                if time.time() - self.last_heartbeat[host] > 3:
                    self.remove_host(host)
                    del self.last_heartbeat[host]

if __name__ == '__main__':
    network_instance = Network()
    network_instance.send_and_receive_heartbeat()