class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class WarningException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class InsufficientBalanceError(ValidationError):
    pass


class InvalidAmountError(ValidationError):
    pass


class BoundaryViolationError(ValidationError):
    pass


class SessionError(ValidationError):
    pass