from abc import ABC, abstractmethod


class IConfiguration(ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> any:
        pass

    @abstractmethod
    def add_dict(self, config: dict[str, any]) -> None:
        """
        Load configuration from dictionary.
        Overrides configuration variables with same names.
        :param config: dictionary with configuration variables.
        """

    @abstractmethod
    def add_json_file(self, file_name: str) -> None:
        """
        Load configuration from json file.
        Overrides configuration variables with same names.
        :param file_name: file path to read json from.
        """
        pass

    @abstractmethod
    def add_environment_variables(self, prefix: str = None) -> None:
        """
        Load configuration from environment variables.
        Overrides configuration variables with same names.
        :param prefix: can filter env variables with prefix.
        """
        pass

    @abstractmethod
    def add_command_line(self, args: list[str]) -> None:
        """
        Load configuration from command line arguments.
        Overrides configuration variables with same names.
        :param args: raw command line arguments.
        """
        pass
