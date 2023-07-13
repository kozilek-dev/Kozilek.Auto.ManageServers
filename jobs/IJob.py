from abc import ABC
from typing import Callable


class IJob(ABC):
    def __init__(self, action: Callable, hours: int, minutes: int, seconds: int) -> None:
        self.action = action
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
