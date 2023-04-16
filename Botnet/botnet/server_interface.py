import abc
from abc import abstractmethod
from typing import Any, List


class ServerInterface(abc.ABC):
    @abstractmethod
    def get_all_bots(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def upload_files(self, *file_path: List[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def download_files(self, *file_path: List[str]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_shell(self,
                  host: str,
                  user: str,
                  password: str,
                  option: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def general_controller(selfself,
                           host: str,
                           user: str,
                           password: str,
                           option: int) -> None:
        raise NotImplementedError()
