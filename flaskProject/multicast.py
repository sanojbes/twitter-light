import socket
import struct
import threading
import time

check_thread_started = False
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

    def send_message(self, message):
        send_thread = threading.Thread(target=self.send_message_thread, args=(message,))
        send_thread.daemon = True  # Setze den Thread als Daemon, um ihn zu beenden, wenn das Hauptprogramm endet
        send_thread.start()

    def send_message_thread(self, message):
        while True:
            self.sock.sendto(message.encode('utf-8'), self.server_address)
            time.sleep(3)

    def receive_messages(self, network):
        global check_thread_started

        while True:
            try:

                data, host = self.sock.recvfrom(1024)
                print(f'Received message: {data.decode("utf-8")} from {host}')

                # Split the message into an array
                message_parts = data.decode("utf-8").split(':')

                # If the first part of the message is 'HB', update the last heartbeat timestamp
                if message_parts[0] == 'HB':
                    network.add_host(message_parts[2])
                    network.last_heartbeat[host] = time.time()


                    if not check_thread_started:
                        check_thread = threading.Thread(target=network.check_heartbeats)
                        check_thread.daemon = True  # Setze den Thread als Daemon, um ihn zu beenden, wenn das Hauptprogramm endet
                        time.sleep(3) # warten bis hb
                        # set leader if given by hb
                        if network.leader is None:
                            print(str(network.leader) + "network leader")
                            if message_parts[3] != 'None':
                                print(str(message_parts[3]) + " message parts 3")
                                network.leader = message_parts[3]
                        #start check heartbeat
                        check_thread.start()
                        check_thread_started = True

            except socket.timeout:
                continue

    def start(self, network):
        thread = threading.Thread(target=self.receive_messages, args=(network,))
        thread.start()

if __name__ == "__main__":
    multicast_group = '224.0.0.100'  # Replace with your chosen multicast group
    server_address = (multicast_group, 10000)  # Replace 10000 with your chosen port number

    client = MulticastClient(multicast_group, server_address)
    client.start()
      
        