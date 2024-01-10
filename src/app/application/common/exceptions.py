class ApplicationException(Exception):
    """Base application exception"""

    @property
    def title(self) -> str:
        return "An application error occurred"


class GatewayError(ApplicationException):
    pass


class DatabaseGatewayError(GatewayError):
    pass


class ObjectStorageGatewayError(GatewayError):
    pass
