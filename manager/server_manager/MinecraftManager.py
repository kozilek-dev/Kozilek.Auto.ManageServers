"""
MinecraftManager.py: Classe responsável por gerenciar os servidores<T>
"""
import logging
from os import getenv
from functools import lru_cache
from random import randint
from time import sleep
from docker import DockerClient
from dotenv import load_dotenv
from ..storage import Storage
from .IMinecraftServer import _IMinecraftServer
from .MinecraftBedRockServer import MinecraftBedRockServer
from .IContainer import IContainer
from .errors import PORT_ALREADY_IN_USE, NAME_ALREADY_IN_USE

logging.basicConfig(
    handlers=[logging.FileHandler(filename='server_manager.log',
                                  encoding='utf-8', mode='a+'),
              logging.StreamHandler()],
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
)


class MinecraftManager:
    """
    Classe responsável por gerenciar os servidores
    """

    def __init__(self):
        load_dotenv()
        self.__host = getenv('DOCKER_HOST')
        self.__docker_instance: DockerClient = DockerClient(base_url=self.__host, tls=False)
        self.__storage = Storage()

    def __transform_env_to_dict(self, env: list[str]) -> dict[str, str]:
        """
        Transforma uma lista de variáveis de ambiente em um dicionário
        """
        env_dict = {}
        keys_to_skip = ['PATH', 'VERSION', 'SERVER_PORT']

        for env_var in env:
            key, value = env_var.split('=')
            if key in keys_to_skip:
                continue
            
            env_dict[key] = value
        return env_dict

    def __create_volume(self, name: str) -> str:
        """
        Cria um volume
        """
        logging.info('Criando volume com nome = %s', name)
        self.__docker_instance.volumes.create(name)
        return name

    def __get_address(self) -> str:
        """
        Retorna o endereço do servidor
        """
        hostname_with_protocol = self.__host.split(':')[1]
        hostname = hostname_with_protocol.split('//')[1]
        return hostname

    def __get_container_port(self, container: IContainer) -> int:
        """
        Retorna a porta do servidor
        """
        default_port = '19132/udp'

        if len(container.ports.keys()) == 0:
            return None

        server_port = container.ports[default_port][1]['HostPort']
        return int(server_port)

    def __get_in_use_ports(self) -> list[int]:
        """
        Retorna as portas em uso pelos servidores
        """
        in_use_ports = []
        containers = self.get_all_servers()
        for container in containers:
            port = self.__get_container_port(container)
            if port is not None:
                in_use_ports.append(port)
        return in_use_ports

    def __check_port(self, port: int):
        """
        Checa se a porta está em uso nos containers
        """
        logging.info('Checando portas em uso nos containers')
        ports_in_use = self.__get_in_use_ports()
        return port in ports_in_use

    def __generate_port(self) -> int:
        """
        Gera uma porta e garante que a mesma não está em uso
        """
        logging.info('Gerando porta...')
        port = randint(19132, 29132)
        while self.__check_port(port):
            port = randint(19132, 29132)
        logging.info('Porta gerada %d', port)
        return port

    def __is_running(self, container: IContainer) -> bool:
        """
        Checa se o container está rodando
        """
        container.reload()
        return container.status in ('running','created')

    def __is_stopped(self, container: IContainer) -> bool:
        """
        Checa se o container está parado
        """
        container.reload()
        return container.status in ('exited', 'created')

    def __exist_container(self, container: IContainer) -> bool:
        """
        Checa se o container existe
        """
        return container is not None

    def get_server_port(self, container: IContainer) -> int:
        """
        Retorna a porta do servidor
        """
        return self.__get_container_port(container)

    @lru_cache(maxsize=1024)
    def create_server(self, server: _IMinecraftServer):
        """
        Cria um servidor
        """
        try:
            image = server.base_image
            
            if server.port is None:
                server.port = self.__generate_port()

            logging.info('Criando servidor com a imagem %s', image)

            volume_name = self.__create_volume(server.name)

            container = self.__docker_instance.containers.run(image,
                                                              "",
                                                              detach=True,
                                                              volumes={volume_name: {
                                                                  'bind': '/data',
                                                                  'mode': 'rw'
                                                              }},
                                                              ports={'19132/udp': server.port},
                                                              name=server.name,
                                                              environment=dict(server.options),
                                                              mem_limit='2G',
                                                              )

            logging.info('Servidor %s criado, id do container %s', container.name, container)
            return container
        except Exception as exception:
            if NAME_ALREADY_IN_USE in str(exception):
                logging.info('O nome %s já está em uso, recuperando container', server.name)
                server = self.get_server(server.name)
                return server

            if PORT_ALREADY_IN_USE in str(exception):
                logging.error('A porta %d já está em uso', server.port)
                return None

            logging.error(str(exception))
            return None

    def get_servers_running(self) -> list:
        """
        Retorna todos os servidores que estão rodando
        """
        logging.info('Listando servidores rodando...')
        return self.__docker_instance.containers.list()

    def get_all_servers(self) -> list:
        """
        Retorna todos os servidores
        """
        logging.info('Listando todos servidores...')
        return self.__docker_instance.containers.list(all=True)

    def get_server(self, identifier: str) -> IContainer:
        """
        Retorna um servidor existente
        """
        try:
            logging.info("Obtendo detalhes do servidor com id = %s", identifier)
            return self.__docker_instance.containers.get(identifier)
        except Exception:
            logging.error('Não foi possível achar o servidor %s', identifier)
            return None

    def stop_server(self, container: IContainer) -> bool:
        """
        Para um servidor
        """
        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return False

        logging.info('Container com status em %s', container.status)
        if self.__is_running(container):
            logging.info('Parando container com id %s', container.id)
            container.kill()
            return True
        return False

    def start_server(self, container: IContainer) -> bool:
        """
        Inicia um servidor
        """
        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return False

        logging.info('Container com status em %s', container.status)
        if self.__is_stopped(container):
            logging.info('Iniciando container com id %s', container.id)
            container.start()
            return True

        if container.status == 'running':
            return True

        return False

    def restart_server(self, container: IContainer) -> bool:
        """
        Reinicia um servidor
        """
        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return False

        logging.info('Reiniciando container com id %s', container.id)
        container.restart()
        return self.__is_running(container)

    def delete_server(self, container: IContainer) -> bool:
        """
        Deleta um servidor
        """
        try:
            if not self.__exist_container(container):
                logging.error('Servidor não existe')
                return False

            container.remove(v=True, force=True)
            logging.info('Servidor %s deletado', container.name)
            return True
        except Exception as exception:
            logging.error(str(exception))
            return False

    def delete_all_servers(self) -> None:
        """
        Deleta todos os servidores
        """
        logging.info('Deletando todos os servidores')

        servers = self.get_all_servers()
        if len(servers) == 0:
            logging.info('Não há servidores para deletar')
            return

        for container in servers:
            logging.info('Deletando servidor %s', container.name)
            self.delete_server(container)

    def run_command(self, container: IContainer, command: str) -> str:
        """
        Executa um comando no servidor
        """
        command = f'send-command {command}'

        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return None
        
        if not self.__is_running(container):
            logging.error('Servidor não está rodando')
            return None

        logging.info('Executando comando %s no servidor %s', command, container.name)
        container.exec_run(command)
        return self.get_last_log(container)

    def set_server_property(self, container: IContainer, prop: str, value: str):
        """
        Define uma propriedade do servidor
        """

        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return None
        
        if not self.__is_running(container):
            logging.error('Servidor não está rodando')
            return None

        exit_code, output = container.exec_run(f'send-command say {prop} definida para {value}',
                                               environment=[f'{prop}={value}'])
        logging.info(output)
        logging.info(exit_code)
        self.restart_server(container)

    def get_logs(self, container: IContainer):
        """
        Retorna os logs do servidor
        """
        logs_in_str = str(container.logs())
        logs_in_lines = logs_in_str.split('\\n')
        return logs_in_lines

    def get_last_log(self, container: IContainer):
        """
        Retorna o último log do servidor
        """
        penultimate_position = -2

        logs = self.get_logs(container)
        last_log = logs[penultimate_position]

        logging.info('Último log obtido')
        logging.info(last_log)

        return last_log

    def backup_server(self, container: IContainer) -> str:
        """
        Copy volume data to storage
        """
        name = container.name
        logging.info('Realizando backup do %s', name)
        self.run_command(container, f'say Realizando backup do {container.name}')
        data, stats = container.get_archive('/data/worlds/')
        logging.info(stats)
        backup_filename = f'{container.name}.tar'

        self.__storage.upload(backup_filename, data)
        logging.info('Backup realizado do servidor %s', name)
        return backup_filename

    def restore_server(self, container: IContainer, backup_id: str) -> bool:
        """
        Copy storage data to volume
        """
        name = container.name
        logging.info('Restaurando servidor %s a partir do backup', name)
        self.run_command(container, f'say Restaurando servidor {container.name} a partir do backup')
        data = self.__storage.download(backup_id)

        response = container.put_archive('/data/', data)
        logging.info('Servidor %s restaurado', name)
        return response

    def is_healthy(self, container: IContainer) -> bool:
        """
        Retorna o status do servidor
        """
        try:
            container.reload()
            return container.attrs['State']['Health']['Status'] == 'healthy'
        except KeyError:
            return False

    def wait_for_healthy(self, container: IContainer) -> bool:
        """
        Espera o servidor ficar saudável
        """
        retries_to_timeout = 6
        current_iteration = 1
        is_healthy = self.is_healthy(container)
        address = self.__get_address()
        port = self.__get_container_port(container)

        while is_healthy is False:
            logging.info('Servidor %s ainda não está saudável...', container.name)
            if current_iteration == retries_to_timeout:
                logging.info('Servidor %s não disponível, com falha', container.name)
                return False

            is_healthy = self.is_healthy(container)
            current_iteration += 1
            sleep(10)
        logging.info('Servidor %s está saudável e pronto para jogar!', (container.name,
                                                                        address, port))
        return True

    def get_all_worlds(self, container: IContainer) -> list[str]:
        """
        Retorna uma lista[str] de mundos contidos no servidor
        """
        empty_name = ''

        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return []

        if self.__is_stopped(container):
            logging.info('Servidor %s está parado, não há mundos', container.name)
            return []

        exit_code, output = container.exec_run('ls /data/worlds/')
        worlds = output.decode('utf-8').split('\n')

        if exit_code != 0:
            logging.error('Erro ao obter mundos do servidor %s', container.name)
            return []

        for world in worlds:
            if world == empty_name:
                worlds.remove(world)

        logging.info('Mundos do servidor %s: %s', container.name, worlds)
        return worlds

    def update_server(self, container: IContainer) -> bool:
        """
        Atualiza um servidor
        """
        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return False
    
        server_config = { 
            'name': container.name,
            'port': self.__get_container_port(container),
            'options': self.__transform_env_to_dict(container.attrs['Config']['Env'])
        }

        self.delete_server(container)

        server = MinecraftBedRockServer(server_config['name'], 
                                        server_config['options'],
                                        server_config['port'])

        created_server = self.create_server(server)
        return created_server is not None

    def get_performance_stats(self, container: IContainer) -> dict:
        """
        Retorna as estatísticas de performance do servidor
        """
        if not self.__exist_container(container):
            logging.error('Servidor não existe')
            return None

        if not self.__is_running(container):
            logging.error('Servidor não está rodando')
            return None

        stats = container.stats(stream=False)

        cpu_usage = stats['cpu_stats']['cpu_usage']['total_usage']
        system_cpu_usage = stats['cpu_stats']['system_cpu_usage']
        memory_usage = stats['memory_stats']['usage']
        network_usage = stats['networks']['eth0']['rx_bytes']
        risk = 0

        cpu_percent = cpu_usage / system_cpu_usage * 100
        memory_percent = memory_usage / stats['memory_stats']['limit'] * 100

        risk = (1.7 * max(0, cpu_percent - 45) + 1 * max(0, memory_percent - 50) / (1.7 + 1))

        logging.info('Estatísticas de performance do servidor %s', container.name)

        return {
            'cpu_percent': float('{:.2f}'.format(cpu_percent)),
            'memory_percent': float('{:.2f}'.format(memory_percent)),
            'saudavel': self.is_healthy(container),
            'risco': float('{:.2f}'.format(risk)),
        }