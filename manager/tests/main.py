from manager import server_manager
import unittest


class ManagerTests(unittest.TestCase):
    __manager = server_manager.MinecraftManager()

    def test_create_server(self):
        mc_server = server_manager.MinecraftServer('mc-unitest', 9999, {'EULA': 'TRUE'})
        self.__manager.delete_server(mc_server)
        created_server = self.__manager.create_server(mc_server)

        self.__manager.delete_server(mc_server)

        self.assertEqual('created', created_server.status)

    def test_stop_server(self):
        mc_server = server_manager.MinecraftServer('mc-unitest', 9999, {'EULA': 'TRUE'})
        self.__manager.create_server(mc_server)

        response = self.__manager.stop_server(mc_server)

        self.__manager.delete_server(mc_server)

        self.assertEqual(True, response)

    def test_start_server(self):
        mc_server = server_manager.MinecraftServer('mc-unitest', 9999, {'EULA': 'TRUE'})
        self.__manager.create_server(mc_server)
        self.__manager.stop_server(mc_server)

        response = self.__manager.start_server(mc_server)

        self.__manager.delete_server(mc_server)

        self.assertEqual(True, response)

    def test_delete_server(self):
        mc_server = server_manager.MinecraftServer('mc-unitest', 9999, {'EULA': 'TRUE'})
        self.__manager.create_server(mc_server)

        response = self.__manager.delete_server(mc_server)

        self.assertEqual(True, response)

    def test_get_server(self):
        expected_name = 'mc-unitest'
        mc_server = server_manager.MinecraftServer('mc-unitest', 9999, {'EULA': 'TRUE'})
        self.__manager.create_server(mc_server)

        response = self.__manager.get_server_running(mc_server.name)

        self.assertEqual(expected_name, response.name)

    def test_list_servers(self):
        mc_server = server_manager.MinecraftServer('mc-unitest', 9999, {'EULA': 'TRUE'})
        self.__manager.create_server(mc_server)

        response = self.__manager.get_servers_running()

        self.__manager.delete_server(mc_server)

        self.assertIsInstance(response, list)
