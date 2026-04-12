class AppException(Exception):
    def __init__(self, message: str):
        self.message: str = message
        super().__init__(message)


class NotFoundError(AppException):
    pass


class ValidationError(AppException):
    pass


class ProcessingError(AppException):
    pass
