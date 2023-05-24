from .IMinecraftServer import _IMinecraftServer


class MinecraftServer(_IMinecraftServer):
    def __init__(self, name: str, port: int, options: dict):
        self.__name = name
        self.__port = port
        self.__options = options

    @property
    def base_image(self) -> str:
        return 'itzg/minecraft-bedrock-server'

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, value: int) -> None:
        self.__port = value

    @property
    def options(self) -> dict:
        return self.__options

    @options.setter
    def options(self, value: int) -> None:
        self.options = value
