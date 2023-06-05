import abc
from typing import Any, Self

from rlscommon.storage.base import Storage

class Configurable(abc.ABC):
    storage: Storage

    @abc.abstractmethod
    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """

    @classmethod
    @abc.abstractmethod
    def from_config(cls, cfg: Any) -> Self:
        r"""
        Build :class:`Self` by provided config
        """

    def to_config(self) -> Any:
        """
        Create config file from current object.
        """