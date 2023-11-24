import socket
import time
import uuid
from datetime import datetime

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

        new_message = "HB:%s:%s" % (
            heartbeat_message["id"],
            heartbeat_message["sender"],
            )
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(new_message.encode(), (MCAST_GRP, MCAST_PORT))
        print(new_message)

        #  self.socket_sender.send_message(
        #  new_message, self.hosts.get_neighbour(), type="unicast"
          #  )

           # logging.info("Heartbeat: send to %s" % self.hosts.get_neighbour())
          #  self.last_heartbeat_sent = get_time()
