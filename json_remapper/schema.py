from typing import Any, Dict, List, Optional
from jsonschema import Draft202012Validator, validators
from json_remapper.exceptions import SchemaValidationError


def extend_with_default(validator_class):
    """Extends JSONSchema validator to fill in default values."""
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema and property not in instance:
                instance[property] = subschema["default"]

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


DefaultValidatingDraft202012Validator = extend_with_default(Draft202012Validator)


class SchemaValidator:
    """Validates and processes JSON schemas."""

    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = DefaultValidatingDraft202012Validator(schema)
        self._anchors: Dict[str, List[str]] = {}
        self._collect_anchors(schema)

    def _collect_anchors(self, schema: Dict[str, Any], path: str = "$") -> None:
        """Collect all anchors in the schema for validation."""
        if isinstance(schema, dict):
            if "$anchor" in schema:
                self._anchors.setdefault(["$anchor"], []).append(path)

            for key, value in schema.items():
                new_path = f"{path}.{key}" if path != "$" else key
                if isinstance(value, (dict, list)):
                    self._collect_anchors(value, new_path)
        elif isinstance(schema, list):
            for i, item in enumerate(schema):
                self._collect_anchors(item, f"{path}[{i}]")

    def validate(self, instance: Dict[str, Any]) -> None:
        """Validate an instance against the schema."""
        errors = []
        for error in self.validator.iter_errors(instance):
            errors.append(
                {
                    "path": ".".join(str(p) for p in error.path),
                    "message": error.message,
                    "schema_path": ".".join(str(p) for p in error.schema_path),
                }
            )

        if errors:
            raise SchemaValidationError(
                f"Schema validation failed with {len(error)} errors", {"errors": errors}
            )

    def get_anchor_paths(self, anchor: str) -> List[str]:
        """Get all paths where an anchor is used"""
        return self._anchors.get(anchor, [])