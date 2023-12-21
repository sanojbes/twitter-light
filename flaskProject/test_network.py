import unittest
from network import Network

class NetworkTest(unittest.TestCase):
    def setUp(self):
        self.network = Network()

    def test_add_host(self):
        self.network.add_host('192.168.0.2')
        self.assertIn('192.168.0.2', self.network.replication_network)

    def test_remove_host(self):
        self.network.remove_host('192.168.0.1')
        self.assertNotIn('192.168.0.1', self.network.replication_network)

    def test_add_client(self):
        self.network.add_client('192.168.1.1')
        self.assertIn('192.168.1.1', self.network.clients_network)

    def test_remove_client(self):
        self.network.remove_client('192.168.1.1')
        self.assertNotIn('192.168.1.1', self.network.clients_network)

    def test_get_hosts(self):
        hosts = self.network.get_hosts()
        self.assertEqual(hosts, ['192.168.0.1', '130.234.204.2', '130.234.203.2', '130.234.204.1', '182.4.3.111'])

    def test_get_client(self):
        clients = self.network.get_client()
        self.assertEqual(clients, [])

    def test_form_ring(self):
        replication_network = ['192.168.0.1', '130.234.204.2', '130.234.203.2', '130.234.204.1', '182.4.3.111']
        ring = self.network.form_ring(replication_network)
        self.assertEqual(ring, ['130.234.203.2', '130.234.204.1', '130.234.204.2', '182.4.3.111', '192.168.0.1'])

    def test_get_neighbour(self):
        ring = ['130.234.203.2', '130.234.204.1', '130.234.204.2', '182.4.3.111', '192.168.0.1']
        neighbour = self.network.get_neighbour(ring, '130.234.204.1', 'right')
        self.assertEqual(neighbour, '130.234.204.2')

    def test_get_ownip(self):
        own_ip = self.network.get_ownip()
        self.assertIsNotNone(own_ip)

    def test_get_network_ip(self):
        network_ip = self.network.get_network_ip()
        self.assertIsNotNone(network_ip)

    def test_get_time(self):
        timestamp = self.network.get_time()
        self.assertIsNotNone(timestamp)

if __name__ == '__main__':
    unittest.main()