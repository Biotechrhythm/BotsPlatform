from collections.abc import Callable

from swiftbots.all_types import (
    IService,
    NotFoundServiceException,
    NotSingleServiceException,
)


class ServiceProvider:
    __services: list[IService]
    __service_factories: list[Callable[[], IService]]

    def __init__(self, service_factories: list[Callable[[], IService]]):
        self.__service_factories = service_factories

    def get_service[T: IService](self, service_type: type[T]) -> T:
        """
        Get a service from dependency injection box.
        :raises NotFoundServiceException: if not found such service in the dependency injection box.
        :raises NotSingleServiceException: if dependency injection box includes more than one 'service_type' services.
        """
        found = list(filter(lambda s: isinstance(s, service_type), self.__services))
        if len(found) == 0:
            raise NotFoundServiceException(f"Not found service {service_type}")
        if len(found) == 1:
            return found[0]
        else:
            raise NotSingleServiceException(f'''More than one service {service_type} found. Use "find_services"''' +
                                            'method instead')

    def find_services[T: IService](self, service_type: type[T]) -> list[T]:
        """
        Find all services in dependency injection box with type 'service_type'.
        """
        found = list(filter(lambda s: isinstance(s, service_type), self.__services))
        return found


class ServiceBuilderBox:
    """
    Container with service factories. They will be instantiated while build application.
    """
    __service_factories: list[Callable[[], IService]]

    def __init__(self):
        self.__service_factories = []

    def add_service(self, service_factory: Callable[[], IService]) -> None:
        """
        Add a service factory for further instantiating while build application.
        """
        self.__service_factories.append(service_factory)

    def get_provider(self) -> ServiceProvider:
        provider = ServiceProvider(self.__service_factories)
        return provider
