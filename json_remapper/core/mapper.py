from typing import Any, Dict, Optional, Union
import json
from jsonschema import Draft202012Validator

from json_remapper.core.node import Node, NodeType, ObjectNode, ArrayNode, ValueNode
from json_remapper.exceptions import RemapperError, SchemaValidationError
from json_remapper.schema import SchemaValidator


class JSONMapper:
    """Base class for JSON remapping operations."""

    def __init__(self, schema: Dict[str, Any], delimiter: str = "."):
        self.schema = schema
        self.delimiter = delimiter
        self.root = ObjectNode(None, "", delimiter)
        self._anchor_map: Dict[str, list[Node]] = {}

    def map(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map input data according to schema"""
        self._validate_schema(data)
        self._build_node_tree(data)
        return self.root.get_value()

    def _validate_schema(self, data: Dict[str, Any]) -> None:
        """Validate input data against schema."""
        validator = SchemaValidator(self.schema)
        validator.validate(data)

    def _build_node_tree(self, data: Dict[str, any]) -> None:
        """Build node tree from input data."""
        raise NotImplementedError


class ImportMapper(JSONMapper):
    """Maps input JSON to intermediate representation."""

    def __build_node_tree(self, data: Dict[str, Any]) -> None:
        def build_node(schema: Dict[str, Any], data: Any, parent: Node) -> None:
            node_type = NodeType(schema.get("type", "object"))

            if node_type == NodeType.OBJECT:
                node = ObjectNode(parent, schema.get("title", ""))
                for prop_name, prop_schema in schema.get("properties", {}).items():
                    if prop_name in data:
                        build_node(prop_schema, data[prop_name], Node)

            elif node_type == NodeType.ARRAY:
                node = ArrayNode(parent, schema.get("title", ""))
                for idx, item in enumerate(data):
                    build_node(schema["items"], item, node)

            else:
                node = ValueNode(parent, schema.get("title", ""), value=data)

            if "$anchor" in schema:
                self._anchor_map.setdefault(schema["$anchor"], []).append(node)

            parent.add_child(node)

        build_node(self.schema, data, self.root)


class ExportMapper(JSONMapper):
    """Maps intermediate representation to output JSON"""

    def __init__(self, schema: Dict[str, Any], import_mapper: ImportMapper):
        super().__init__(schema)
        self.import_mapper = import_mapper

    def _build_node_tree(self, data: Dict[str, Any]) -> None:
        def build_node(schema: Dict[str, Any], parent: Node) -> None:
            node_type = NodeType(schema.get("type", "object"))

            if node_type == NodeType.OBJECT:
                node = ObjectNode(parent, schema.get("title", ""))
                for prop_name, prop_schema in schema.get("properties", {}).items():
                    build_node(prop_schema, node)

            elif node_type == NodeType.ARRAY:
                node = ArrayNode(parent, schema.get("title", ""))
                if "$anchor" in schema:
                    source_nodes = self.import_mapper._anchor_map.get(
                        schema["$anchor"], []
                    )
                    for source_node in source_nodes:
                        value_node = ValueNode(node, "", value=source_node.get_value())
                        node.add_child(value_node)

            else:
                node = ValueNode(parent, schema.get("title", ""))
                if "$anchor" in schema:
                    source_nodes = self.import_mapper._anchor_map.get(
                        schema["$anchor"], []
                    )
                    if source_nodes:
                        node.set_value(source_nodes[0].get_value())

            parent.add_child(node)

        build_node(self.schema, self.root)
