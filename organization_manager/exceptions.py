class BaseError(Exception):
    """Base class for exceptions in this module."""
    pass


class DatabaseCreationError(BaseError):
    """Exception raised for errors in the database creation process."""

    def __init__(self, message="Failed to create the organization database"):
        self.message = message
        super().__init__(self.message)


class OrganizationCreationError(BaseError):
    """Exception raised for errors during the organization creation."""

    def __init__(self, message="Failed to create the organization"):
        self.message = message
        super().__init__(self.message)
