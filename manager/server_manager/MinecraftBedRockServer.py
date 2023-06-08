"""
Módulo para gerenciar um servidor Minecraft BedRock
"""
import re
from typing import Optional
from .IMinecraftServer import _IMinecraftServer


class MinecraftBedRockServer(_IMinecraftServer):
    """
    Classe para gerenciar um servidor Minecraft BedRock
    """
    def __init__(self, name: str, options: Optional[dict]):
        self.__name = name
        self.__port = 19132
        self.__options = {'EULA': True} if options is None else options

    @staticmethod
    def spell_name(name):
        """
        Transforma o nome do servidor em um nome válido para o Docker
        """
        name = re.sub(r'[^a-z0-9-]', '', name.lower())
        name = re.sub(r'-+', '-', name)
        name = name.strip('-')
        return name

    @property
    def base_image(self) -> str:
        return 'itzg/minecraft-bedrock-server'

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value) -> None:
        self.__name = self.spell_name(value)

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, value: int) -> None:
        if 19132 < value < 29132:
            self.__port = value

    @property
    def options(self) -> dict:
        return self.__options

    @options.setter
    def options(self, value: int) -> None:
        self.options = value
