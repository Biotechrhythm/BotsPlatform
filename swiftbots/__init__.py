from swiftbots.all_types import ILoggerFactory
from swiftbots.bots_application import BotsApplicationBuilder


def initialize_app(logger_factory: ILoggerFactory | None = None) -> BotsApplicationBuilder:
    bot_app_builder = BotsApplicationBuilder(logger_factory)
    return bot_app_builder
