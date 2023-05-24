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

    @property
    @abstractmethod
    def port(self) -> int:
        pass

    @property
    @abstractmethod
    def options(self) -> int:
        pass
