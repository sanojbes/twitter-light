import threading
import time
import socket

class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.replication_network = []  # List of hosts in the network
        self.last_heartbeat = {}  # Stores the last heartbeat timestamp from each host
        self.leader = None  # The leader host
        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.check_heartbeats).start()

    def receive_messages(self):
        while True:
            try:
                data, host = self.sock.recvfrom(1024)
                print(f'Received message: {data.decode("utf-8")} from {host}')

                # Split the message into an array
                message_parts = data.decode("utf-8").split(':')

                # If the first part of the message is 'HB', update the last heartbeat timestamp
                if message_parts[0] == 'HB':
                    self.last_heartbeat[host] = time.time()

            except socket.timeout:
                continue

    def check_heartbeats(self):
        while True:
            time.sleep(1)  # Check heartbeats every second
            for host in list(self.last_heartbeat.keys()):
                if time.time() - self.last_heartbeat[host] > 3:  # No heartbeat within the last 3 seconds
                    self.remove_host(host)
                    del self.last_heartbeat[host]
                    if host == self.leader:  # If the leader is not sending a heartbeat
                        self.elect_leader()  # Trigger a leader election

    def elect_leader(self):
        """
        Elects a new leader host using the Bully Algorithm.
        """
        if self.replication_network:  # Check if there are any hosts in the network
            self.leader = max(self.replication_network)  # The host with the highest ID becomes the leader

    def add_host(self, host):
        """
        Adds a new host to the network and triggers a leader election.
        """
        if host not in self.replication_network:
            self.replication_network.append(host)
            self.elect_leader()
        else:
            print(f"Host {host} was already discovered")

    def remove_host(self, host):
        """
        Removes a host from the network and triggers a leader election if the leader was removed.
        """
        if host in self.replication_network:
            self.replication_network.remove(host)
            if host == self.leader:
                self.elect_leader()