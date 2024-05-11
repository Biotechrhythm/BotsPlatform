from abc import ABC
from typing import TYPE_CHECKING

from swiftbots.all_types import IService

if TYPE_CHECKING:
    from swiftbots.bots import Bot


class IAppRunner(IService, ABC):
    def run(self, bots: list["Bot"]) -> None:
        pass
