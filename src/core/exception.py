from datetime import date


class AppException(Exception):
    def __init__(
        self, message: str, status_code: int = 500, details: dict | None = None
    ):
        self.message: str = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ValidationError(AppException):
    pass


class ProcessingError(AppException):
    pass


class SessionConflictError(AppException):
    def __init__(
        self,
        message: str,
        dates: list[date],
        formateur_conflict: bool,
        salle_conflict: bool,
    ):
        super().__init__(
            message,
            status_code=409,
            details={
                "dates": dates,
                "formateur_conflict": formateur_conflict,
                "salle_conflict": salle_conflict,
            },
        )
