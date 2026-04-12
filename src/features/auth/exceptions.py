from src.core.exception import AppException, ValidationError


class UserAlreadyExistsError(ValidationError):
    def __init__(self, email: str):
        super().__init__(message=f"User with email {email} Already Exists")
