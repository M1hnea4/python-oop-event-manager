"""
Defines custom exceptions for the repository layer.
"""

class RepositoryException(Exception):
    """
    Base class for repository errors.
    Raised for issues like duplicate IDs or non-existent entities.
    """
    pass