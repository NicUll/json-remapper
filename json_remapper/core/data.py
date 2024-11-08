from typing import Any, Dict, List, Optional, Union
from collections import defaultdict


class Data:
    """Wrapper class for handling data during mapping operations."""

    def __init__(self, value: Any):
        self._value = value

    @property
    def value(self) -> Any:
        return self._value

    def get(self, key: str, default: Any = None) -> "Data":
        """Get a nested value using dot notation."""
        current = self._value
        for part in key.split("."):
            if isinstance(current, dict):
                current = current.get(part, default)
            else:
                return Data(default)
        return Data(current)

    def set(self, key: str, value: Any) -> None:
        """Set a nested value using dot notation."""
        parts = key.split(".")
        current = self._value
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def map(self, func) -> "Data":
        """Apply a function to the value."""
        if isinstance(self._value, list):
            return Data([func(item) for item in self._value])
        return Data(func(self._value))

    def filter(self, predicate) -> "Data":
        """Filter items in a list."""
        if isinstance(self._value, list):
            return Data([item for item in self._value if predicate(item)])
        return self

    def __repr__(self) -> str:
        return f"Data({self._value!r})"
