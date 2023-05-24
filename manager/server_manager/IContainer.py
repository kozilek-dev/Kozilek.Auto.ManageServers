from abc import ABC, abstractmethod
from typing import Optional

class IContainer(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def status(self):
        pass

    @property
    @abstractmethod
    def ports(self):
        pass

    @property
    @abstractmethod
    def attrs(self):
        pass

    @abstractmethod
    def remove(self, **kwargs):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def get_archive(self, path: str):
        pass

    @abstractmethod
    def put_archive(self, path: str, data):
        pass

    @abstractmethod
    def exec_run(self, command: str, environment: Optional[dict]):
        pass

    @abstractmethod
    def logs(self):
        pass

    @abstractmethod
    def kill(self):
        pass

    @abstractmethod
    def reload(self):
        pass