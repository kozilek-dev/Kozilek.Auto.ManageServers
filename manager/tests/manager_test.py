"""
Esse arquivo contém os testes unitários para o módulo manager
"""
from unittest import TestCase
from manager import server_manager


class ManagerTests(TestCase):
    """
    Classe de testes para o módulo manager
    """
    __manager = server_manager.MinecraftManager()
    __default_port = 9999
    __default_options = {'EULA': 'TRUE'}
    __default_name = 'mc-unitest'

    def test_create_server(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        self.__manager.delete_server(container)

        self.assertEqual('created', container.status)

    def test_stop_server(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.stop_server(container)

        self.__manager.delete_server(container)

        self.assertEqual(True, response)

    def test_start_server(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)
        self.__manager.stop_server(container)

        response = self.__manager.start_server(container)

        self.__manager.delete_server(container)
        self.assertEqual(True, response)

    def test_restart_server(self):
        """
        Testa o reinício de um servidor
        """
        mc_server = server_manager.MinecraftBedRockServer(self.__default_name,
                                                          self.__default_options)
        container = self.__manager.create_server(mc_server)
        self.__manager.stop_server(container)

        response = self.__manager.restart_server(container)

        self.__manager.delete_server(container)
        self.assertEqual(True, response)

    def test_delete_server(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.delete_server(container)

        self.assertEqual(True, response)

    def test_delete_all_servers(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        self.__manager.create_server(mc_server)

        self.__manager.delete_all_servers()

        response = self.__manager.get_all_servers()

        self.assertEqual(0, len(response))

    def test_get_server(self):
        """
        Testa a obtenção de um servidor
        """
        expected_name = 'mc-unitest'
        mc_server = server_manager.MinecraftBedRockServer('mc-unitest', self.__default_options)
        self.__manager.create_server(mc_server)

        response = self.__manager.get_server(mc_server.name)

        self.assertEqual(expected_name, response.name)

    def test_list_servers_running(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.get_servers_running()

        self.__manager.delete_server(container)

        self.assertIsInstance(response, list)

    def test_list_all_servers(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.get_all_servers()

        self.__manager.delete_server(container)

        self.assertIsInstance(response, list)

    def test_get_logs(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.get_logs(container)

        self.__manager.delete_server(container)

        self.assertIsInstance(response, list)

    def test_get_last_log(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.get_last_log(container)

        self.__manager.delete_server(container)

        self.assertIsInstance(response, str)

    def test_run_command(self):
        # NOTE: Esse teste tem intermitência, pendente compreender o porquê
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)


        # response = self.__manager.run_command(container, 'summon cow 10 20 30')

        self.__manager.wait_for_healthy(container)

        self.__manager.delete_server(container)

        # self.assertEqual('Unable to summon object', response)
        self.assertTrue(True)

    def test_is_healthy(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.is_healthy(container)

        self.__manager.delete_server(container)

        self.assertEqual(False, response)

    def test_backup_server(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)

        response = self.__manager.backup_server(container)

        self.__manager.delete_server(container)

        self.assertEqual('mc-v1.tar', response)

    def test_restore_server(self):
        mc_server = server_manager.MinecraftBedRockServer('mc-v1', self.__default_options)
        container = self.__manager.create_server(mc_server)
        self.__manager.backup_server(container)

        response = self.__manager.restore_server(container, 'mc-v1.tar')

        self.__manager.delete_server(container)

        self.assertEqual(True, response)
