"""
Defines custom exceptions for the validation layer.
"""

class ValidationException(Exception):
    """
    Base class for all validation errors.
    Raised when entity data fails validation checks.
    """
    pass