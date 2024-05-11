class StartBotException(BaseException):
    pass


class ExitApplicationException(BaseException):
    pass


class ExitBotException(BaseException):
    pass


class RestartListeningException(BaseException):
    pass


class NotFoundServiceException(Exception):
    pass


class NotSingleServiceException(Exception):
    pass


class NoBotsException(Exception):
    pass
