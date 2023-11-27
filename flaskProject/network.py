import socket
import time
import uuid
from datetime import datetime

class network:
    clients_network = []
    replication_network= []
    replication_sorted_network = []
def __init__(self, current_member_ip):
    print("Network initialized")
    self.current_member_ip = current_member_ip
    self.add_host(self.current_member_ip)

def add_host(self, host):
    if host not in self. replication_network:
            self. replication_network.append(host)
            self.sorted_ring = self._form_ring(self. replication_network)
    else:
        print("Host %s was already discovered" % host)

    def remove_host(self, host):
        if host in self. replication_network:
            self. replication_network.remove(host)
            self.sorted_ring = self._form_ring(self. replication_network)
        else:
            print("Host %s was already removed" % host)

    def add_client(self, host):
        if host not in self.clients_network:
            self.clients_network.append(host)
        else:
           print("Client %s was already added" % host)

    def get_hosts(self):
        return self. replication_network


def get_ownip():
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    return ip_address
def get_time():
    timest=0
    timest = time.time()
    date_time = datetime.fromtimestamp(timest)
    date_time.strftime("%Y-%m-%d %H:%M:%S")
    print( date_time.strftime("%Y-%m-%d %H:%M:%S"))
    return timest
def send_heartbeat():
     # create heartbeat message and send it every 3 sec.
     time_diff = get_time() - 1700835784 #self.last_heartbeat_sent
     MCAST_GRP = '224.1.1.1'
     MCAST_PORT = 5007

     if time_diff >= 3:
        heartbeat_message = {
            "id": str(uuid.uuid4()),
            "sender": get_ownip(),
            "timestamp": get_time(),
        }

        heartbeat_msg = "HB:%s:%s" % (
            heartbeat_message["id"],
            heartbeat_message["sender"],
            )
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(heartbeat_msg.encode(), (MCAST_GRP, MCAST_PORT))
        print(heartbeat_msg)
        return heartbeat_msg