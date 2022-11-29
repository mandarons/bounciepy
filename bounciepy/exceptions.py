class BouncieException(Exception):
    pass


class BadRequestError(BouncieException):
    def __init__(self, *args: object) -> None:
        self.message = args[0]
        print(self.message)
        super().__init__(*args)


class UnauthorizedError(BouncieException):
    def __init__(self, *args: object) -> None:
        self.message = "Error: Invalid or expired access token."
        print(self.message)
        super().__init__(*args)


class NotFoundError(BouncieException):
    def __init__(self, *args: object) -> None:
        self.message = "Error: resource  not found."
        print(self.message)
        super().__init__(*args)


class ForbiddenError(BouncieException):
    def __init__(self, *args: object) -> None:
        self.message = args[0]
        print(self.message)
        super().__init__(*args)


class InternalError(BouncieException):
    def __init__(self, response, *args: object) -> None:
        self.message = response.text()
        print(self.message)
        super().__init__(*args)
