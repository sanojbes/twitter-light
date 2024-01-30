import socket
import struct
import threading
import time

class MulticastClient:
    def __init__(self, multicast_group, server_address):
        self.server_address = server_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.2)

        # Bind to the wildcard address
        self.sock.bind(('', server_address[1]))

        # Tell the operating system to add the socket to the multicast group
        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def send_message(self, network):
        send_thread = threading.Thread(target=self.send_message_thread, args=(network,))
        send_thread.daemon = True  # Setze den Thread als Daemon, um ihn zu beenden, wenn das Hauptprogramm endet
        send_thread.start()

    def send_message_thread(self, network):
        while True:
            message = network.create_message()
            self.sock.sendto(message.encode('utf-8'), self.server_address)
            time.sleep(1)

    def receive_messages(self, network):
        while True:
            try:
                data, host = self.sock.recvfrom(1024)
                #print(f'Received message: {data.decode("utf-8")} from {host}')

                # Split the message into an array
                message_parts = data.decode("utf-8").split(':')

                # If the first part of the message is 'HB', update the last heartbeat timestamp
                if message_parts[0] == 'HB':
                    # set leader if given by hb
                    if message_parts[3] != 'None':
                        network.leader = message_parts[3]
                        print('LEADER AUS HB: ' + network.leader)

                    network.add_host(message_parts[2])
                    network.last_heartbeat[host] = time.time()
                    network.check_heartbeats()



            except socket.timeout:
                continue

    def start(self, network):
        thread = threading.Thread(target=self.receive_messages, args=(network,))
        thread.start()
      
        