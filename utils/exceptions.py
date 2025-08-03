"""
Custom exceptions for Team Project Planner.
Industry standard exception hierarchy with meaningful error messages.
"""

class TeamPlannerException(Exception):
    """Base exception class for Team Project Planner."""
    pass

class ValidationError(TeamPlannerException):
    """Raised when input validation fails."""
    pass

class ResourceNotFoundError(TeamPlannerException):
    """Raised when a requested resource is not found."""
    pass

class DuplicateResourceError(TeamPlannerException):
    """Raised when attempting to create a duplicate resource."""
    pass

class BusinessRuleViolationError(TeamPlannerException):
    """Raised when a business rule is violated."""
    pass

class DataPersistenceError(TeamPlannerException):
    """Raised when data persistence operations fail."""
    pass

class UnauthorizedOperationError(TeamPlannerException):
    """Raised when an unauthorized operation is attempted."""
    pass
