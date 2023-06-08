"""
Interface para um container, da biblioteca Python Docker SDK
"""

from abc import ABC, abstractmethod
from typing import Optional

class IContainer(ABC):
    """
    Interface para um container, da biblioteca Python Docker SDK
    """
    @property
    @abstractmethod
    def id(self):
        """
        Id do container
        """

    @property
    @abstractmethod
    def name(self):
        """
        Nome do container
        """

    @property
    @abstractmethod
    def status(self):
        """
        Status do container
        """

    @property
    @abstractmethod
    def ports(self):
        """
        Portas do container
        """

    @property
    @abstractmethod
    def attrs(self):
        """
        Atributos do container
        """

    @abstractmethod
    def remove(self, **kwargs):
        """
        Remove o container
        """

    @abstractmethod
    def start(self):
        """
        Inicia o container
        """

    @abstractmethod
    def stop(self):
        """
        Para o container
        """

    @abstractmethod
    def restart(self):
        """
        Reinicia o container
        """

    @abstractmethod
    def get_archive(self, path: str):
        """
        Retorna um arquivo do container
        """

    @abstractmethod
    def put_archive(self, path: str, data):
        """
        Envia um arquivo para o container
        """

    @abstractmethod
    def exec_run(self, command: str, environment: Optional[dict]):
        """
        Executa um comando no container
        """

    @abstractmethod
    def logs(self):
        """
        Retorna os logs do container
        """

    @abstractmethod
    def kill(self):
        """
        Encerra o container
        """

    @abstractmethod
    def reload(self):
        """
        Recarrega o status do container
        """
