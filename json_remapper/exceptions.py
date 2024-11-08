from typing import Any, Dict, Optional


class RemapperError(Exception):
    """Base exception for JSON remapper errors."""

    pass


class SchemaValidationError(RemapperError):
    """Raised when schema validation fails."""

    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.errors = errors or {}


class MappingError(RemapperError):
    """Raised when mapping operation fails."""

    pass


class AnchorNotFoundError(RemapperError):
    """Raised when a referenced anchor is not found."""

    pass
