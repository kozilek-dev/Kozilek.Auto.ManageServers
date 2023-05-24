from abc import ABC, abstractmethod


class _IMinecraftServer(ABC):
    @property
    @abstractmethod
    def base_image(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    def name(self, value) -> None:
        pass

    @property
    @abstractmethod
    def port(self) -> int:
        pass

    @port.setter
    @abstractmethod
    def port(self, value) -> int:
        pass

    @property
    @abstractmethod
    def options(self) -> dict:
        pass

    @options.setter
    @abstractmethod
    def options(self, value) -> None:
        pass
