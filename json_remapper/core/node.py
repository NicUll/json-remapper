from enum import Enum
from typing import Any, Optional, Union, Dict, List


class NodeType(Enum):
    NODE = "node"
    ROOT = "root"
    ARRAY = "array"
    OBJECT = "object"
    STRING = "string"
    BOOLEAN = "boolean"
    INTEGER = "integer"
    NUMBER = "number"


class Node:
    """Base node class representing a JSON node in the remapping tree."""

    def __init__(
        self, parent: Optional["Node"], path: str, delimiter: str = ""
    ) -> None:
        self.parent = parent
        self._relative_path: str = path
        self.delimiter: str = delimiter
        self.child: Optional[Node] = None

    def get_value(self) -> Any:
        """Get the value of this node."""
        if self.child:
            return self.child.get_value()
        return None

    def get_path(self) -> str:
        """Get the full path to this node."""
        if self.parent:
            parent_path = self.parent.get_path()
            return (
                f"{parent_path}{self.delimiter}{self._relative_path}"
                if parent_path
                else self._relative_path
            )
        return self._relative_path

    def add_child(self, child: "Node") -> "Node":
        """Add a child node."""
        self.child = child
        return child

    def remove(self) -> None:
        """Remove this node from its parent."""
        if self.parent:
            self.parent._remove_child(self)

    def _remove_child(self, child: "Node") -> None:
        """Remove a child node."""
        if self.child is child:
            self.child = None


class ObjectNode(Node):
    """Node representing a JSON object."""

    def __init__(self, parent: Optional[Node], path: str, delimiter: str = "") -> None:
        super().__init__(parent, path, delimiter)
        self.children: Dict[str, Node] = {}
        self.inactive: List[str] = []

    def add_child(self, child: Node) -> Node:
        self.children[child._relative_path] = child
        return child

    def get_value(self) -> dict:
        result = {}
        for key, child in self.children.items():
            if key not in self.inactive:
                value = child.get_value()
                if value is not None:
                    result[key] = value
        return result

class ArrayNode(Node):
    """Node representing a JSON array."""

    def __init__(self, parent: Optional[Node], path: str, delimiter: str = "") -> None:
        super().__init__(parent, path, delimiter)
        self.children: Dict[str, Node] = {}
        
    def get_value(self) -> list:
        return [child.get_value() for child in self.children.values() if child.get_value() is not None]
    
class ValueNode(Node):
    """Node representing a JSON value (string, number, boolean, null)."""

    def __init__(self, parent: Optional[Node], path: str, delimiter: str = "", value: Any = None) -> None:
        super().__init__(parent, path, delimiter)
        self.value = value
        
    def get_value(self) -> Any:
        return self.value
    
    def set_value(self, value: Any) -> None:
        self.value = value