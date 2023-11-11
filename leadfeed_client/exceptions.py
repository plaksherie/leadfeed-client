

class ClientException(BaseException):
    """
    This is raised when unknown exceptions occur.

    And it's used as a base for all other exceptions
    so if you want to catch all GitHub related errors
    you should catch this base exception.
    """


class ClientConnectionException(ClientException):
    """This is raised when there is a connection issue with GitHub."""
