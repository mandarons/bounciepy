class BouncieException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = args[0]
        super().__init__(*args)


class BadRequestError(BouncieException):
    pass


class UnauthorizedError(BouncieException):
    pass


class NotFoundError(BouncieException):
    pass


class ForbiddenError(BouncieException):
    pass


class InternalError(BouncieException):
    pass
