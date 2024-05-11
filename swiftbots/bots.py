from traceback import format_exc

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from swiftbots.all_types import (
    IController,
    ILogger,
    ILoggerFactory,
    IMessageHandler,
    IService,
    ITask,
    IView,
)


class Bot:
    """A storage of controllers and views"""

    name: str
    __logger: ILogger
    __db_session_maker: async_sessionmaker[AsyncSession] | None = None

    view_class: type[IView] | None
    controller_classes: list[type[IController]]
    task_classes: list[type[ITask]] | None
    message_handler_class: type[IMessageHandler] | None

    view: IView | None = None
    controllers: list[IController]
    tasks: list[ITask] | None = None
    message_handler: IMessageHandler | None

    @property
    def logger(self) -> ILogger:
        return self.__logger

    @property
    def db_session_maker(self) -> async_sessionmaker[AsyncSession] | None:
        return self.__db_session_maker

    def __init__(
        self,
        controller_classes: list[type[IController]],
        view_class: type[IView] | None,
        task_classes: list[type[ITask]] | None,
        message_handler_class: type[IMessageHandler] | None,
        logger_factory: ILoggerFactory,
        name: str,
        db_session_maker: async_sessionmaker | None,
    ):
        self.view_class = view_class
        self.controller_classes = controller_classes
        self.task_classes = task_classes
        self.message_handler_class = message_handler_class
        self.name = name
        self.__logger = logger_factory.get_logger()
        self.__logger.bot_name = self.name
        self.__db_session_maker = db_session_maker


async def soft_close_bot_async(bot: Bot) -> None:
    """
    Close softly bot's view and tasks to close all connections (like database or http clients)
    """
    if bot.tasks:
        for task in bot.tasks:
            try:
                await task._soft_close_async()
            except Exception as e:
                await bot.logger.error_async(
                    f"Raised an exception `{e}` when a task closing method called:\n{format_exc()}"
                )
    if bot.view:
        try:
            await bot.view._soft_close_async()
        except Exception as e:
            await bot.logger.error_async(
                f"Raised an exception `{e}` when a bot closing method called:\n{format_exc()}"
            )
