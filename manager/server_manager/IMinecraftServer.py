"""
Interface para um servidor de Minecraft
"""
from abc import ABC, abstractmethod


class _IMinecraftServer(ABC):
    @property
    @abstractmethod
    def base_image(self) -> str:
        """
        Imagem base do servidor
        """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Nome do servidor
        """

    @name.setter
    def name(self, value) -> None:
        """
        Nome do servidor
        """

    @property
    @abstractmethod
    def port(self) -> int:
        """
        Porta do servidor
        """

    @port.setter
    @abstractmethod
    def port(self, value) -> int:
        """
        Porta do servidor
        """

    @property
    @abstractmethod
    def options(self) -> dict:
        """
        Opções do servidor
        """

    @options.setter
    @abstractmethod
    def options(self, value) -> None:
        """
        Opções do servidor
        """
