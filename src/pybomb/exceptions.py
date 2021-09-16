"""Exceptions used in this library."""


class PybombException(Exception):
    """Base Exception for library."""

    pass


class ClientException(PybombException):
    """Base Client Exception for module."""

    pass


class InvalidReturnFieldException(ClientException):
    """Exception for invalid return fields."""

    pass


class InvalidSortFieldException(ClientException):
    """Exception for invalid sort fields."""

    pass


class InvalidFilterFieldException(ClientException):
    """Exception for invalid filter fields."""

    pass


class InvalidResponseException(ClientException):
    """Exception thrown when receiving an invalid response from selected resource."""

    pass


class BadRequestException(ClientException):
    """Exception thrown when attempting to send a bad request."""

    pass


class InvalidClientException(ClientException):
    """Exception thrown when attempting to import a non-defined client."""

    pass
