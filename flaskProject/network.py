import threading
import time
import socket
import uuid
import json
import multicast
import requests



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
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.replication_network = []  # List of hosts in the network
        self.last_heartbeat = {}  # Stores the last heartbeat timestamp from each host
        self.leader = None  # The leader host
        threading.Thread(target=self.check_heartbeats).start()

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
        #else:
            #print(f"Client {host} was already added")

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
        else:
            return "Keine IP-Adresse gefunden"
    @staticmethod   
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

    def check_first_host(self):
        time.sleep(2)
        if self.leader is None:
            self.elect_leader()
            print('INITIAL LEADER ELECTED: ' + str(self.leader))



    def check_heartbeats(self):
        for host in list(self.last_heartbeat.keys()):
            if time.time() - self.last_heartbeat[host] > 2:  # No heartbeat within the last 2 seconds
                self.remove_host(host)

                del self.last_heartbeat[host]

    def elect_leader(self):
        """
        Elects a new leader host using the Bully Algorithm.
        """
        if self.replication_network:  # Check if there are any hosts in the network
            self.leader = max(self.replication_network)  # The host with the highest ID becomes the leader


    def add_host(self, host):
        """
        Adds a new host to the network
        """
        if host not in self.replication_network:
            self.replication_network.append(host)
            print('Added new host: ' + host)
            print('Current hosts: ' + str(self.replication_network))


    def remove_host(self, host):
        """
        Removes a host from the network and triggers a leader election if the leader was removed.
        """
        if host[0] in self.replication_network:
            print('List before Host gets deleted: ' + str(self.replication_network))
            self.replication_network.remove(host[0])
            print('List after Host gets deleted: ' + str(self.replication_network))
            if host[0] == self.leader:
                self.elect_leader()
                print('ELECT NEW LEADER: ' +str(self.leader))

    def create_message(self):
        heartbeat_message = {
            "id": str(uuid.uuid4()),
            "sender": self.get_network_ip(),
            "leader": self.leader,
        }
        heartbeat_msg = f"HB:{heartbeat_message['id']}:{heartbeat_message['sender']}:{heartbeat_message['leader']}"

        return heartbeat_msg

    def create_update_message(self):
        with open('users.json', 'r') as file:
            users_json = json.load(file)
        users_string = json.dumps(users_json)

        return users_string



    def update_Json(self):
        users_string = self.create_update_message()
        for server in self.replication_network:
            requests.post(f'http://{server}:5000/update-users', data=users_string)
            print('updated data in server: ' + str(server))