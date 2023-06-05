import abc
from dataclasses import dataclass, field
from typing import Any, Self


@dataclass(slots=True)
class DataRow:
    target: str
    variable: str
    source: str
    value: Any | None = field(default=None, compare=False)


class Storage(abc.ABC):
    @abc.abstractmethod
    def store(self, source: str, value: Any) -> None:
        pass

    @abc.abstractmethod
    async def get(self, target: str) -> dict[str, Any]:
        pass

    @abc.abstractmethod
    def add_dependency(self, target: str, variable: str, source: str) -> None:
        pass

    @abc.abstractmethod
    def remove_dependency(self, target: str, variable: str, source: str) -> None:
        pass

    @abc.abstractmethod
    def save(self, path: str | None = None) -> None:
        pass

    @abc.abstractmethod
    def show(self):
        pass

    @classmethod
    @abc.abstractmethod
    def from_config(cls, cfg) -> Self:
        pass
