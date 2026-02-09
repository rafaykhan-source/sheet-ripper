import csv
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Writer(ABC):
    @abstractmethod
    def write(self, path: str, data: list[list[str]]) -> None:
        pass


@dataclass
class CSVWriter(Writer):
    def __post_init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def write(self, path: str, data: list[list[str]]):
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(data)
