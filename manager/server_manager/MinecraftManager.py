from docker import DockerClient
from .IMinecraftServer import _IMinecraftServer
from .errors import PORT_ALREADY_IN_USE, NAME_ALREADY_IN_USE
import logging


logging.basicConfig(level=logging.INFO)


class MinecraftManager(object):
    def __init__(self, ):
        self.__docker_instance: DockerClient = DockerClient(base_url='tcp://52.255.205.194:2375', tls=False)

    def get_servers_running(self) -> DockerClient.containers:
        logging.info(f'Listando servidores...')
        return self.__docker_instance.containers.list()

    def get_server_running(self, identifier: str):
        try:
            logging.info(f'Tentando obter detalhes do servidor com id = {identifier}')
            return self.__docker_instance.containers.get(identifier)
        except Exception:
            logging.error(f'Não foi possível achar o servidor {identifier}')
            return None

    def __create_volume(self, name: str) -> str:
        logging.info(f'Criando volume com nome = {name}')
        self.__docker_instance.volumes.create(name)
        return name

    def create_server(self, server: _IMinecraftServer):
        try:
            image = server.base_image

            logging.info(f'Criando servidor com a imagem {image}')

            volume_name = self.__create_volume(server.name)

            container = self.__docker_instance.containers.run("itzg/minecraft-bedrock-server",
                                                             "",
                                                             detach=True,
                                                             volumes={volume_name: {
                                                                 'bind': '/data',
                                                                 'mode': 'rw'
                                                             }},
                                                             ports={'19132/udp': server.port},
                                                             name=server.name,
                                                             environment=server.options
                                                             )

            logging.info(f'Servidor {server.name} criado, id do container {container.id}')
            return container
        except Exception as exception:
            if NAME_ALREADY_IN_USE in str(exception):
                return self.get_server_running(server.name)

            if PORT_ALREADY_IN_USE in str(exception):
                logging.error(f'A porta {server.port} já está em uso')

    def stop_server(self, server: _IMinecraftServer) -> bool:
        container = self.get_server_running(server.name)

        if container is None:
            return False

        if (container.status == 'running') or (container.status == 'created'):
            logging.info(f'Parando container com id {container.id}')
            container.kill()
            return True
        return False

    def start_server(self, server: _IMinecraftServer) -> bool:
        container = self.get_server_running(server.name)

        if container is None:
            return False

        if (container.status == 'exited') or (container.status == 'created'):
            logging.warning(f'Iniciando container com id {container.id}')
            container.start()
            return True
        return False

    def delete_server(self, server: _IMinecraftServer) -> bool:
        container = self.get_server_running(server.name)

        if container is None:
            return False

        try:
            container.remove(v=True, force=True)
            return True
        except Exception:
            return False