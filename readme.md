# JSON Remapper

A flexible and powerful JSON schema-based remapping tool that allows you to transform JSON data structures using JSON Schema definitions.

## Features

- Schema-based JSON transformation
- Support for complex nested structures
- Validation of input and output schemas
- Anchor-based value mapping
- Support for arrays, objects, and primitive values
- Type safety and validation

## Installation

```bash
pip install json-remapper
```

## Quick Start

```python
from json_remapper import JSONMapper, ImportMapper, ExportMapper

# Define your input schema
input_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "$anchor": "user_name"
        },
        "details": {
            "type": "object",
            "properties": {
                "age": {
                    "type": "integer",
                    "$anchor": "user_age"
                }
            }
        }
    }
}

# Define your output schema
output_schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "fullName": {
                    "type": "string",
                    "$anchor": "user_name"
                },
                "years": {
                    "type": "integer",
                    "$anchor": "user_age"
                }
            }
        }
    }
}

# Your input data
input_data = {
    "name": "John Doe",
    "details": {
        "age": 30
    }
}

# Create mappers
import_mapper = ImportMapper(input_schema)
export_mapper = ExportMapper(output_schema, import_mapper)

# Transform the data
intermediate = import_mapper.map(input_data)
result = export_mapper.map(intermediate)

print(result)
# Output: {'user': {'fullName': 'John Doe', 'years': 30}}
```

## Schema Definition

The remapper uses JSON Schema with an additional `$anchor` property to define mapping relationships. An anchor in the input schema can be referenced in the output schema to map values.

### Input Schema Example
```json
{
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "$anchor": "product_title"
        },
        "variants": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sku": {
                        "type": "string",
                        "$anchor": "variant_sku"
                    }
                }
            }
        }
    }
}
```

### Output Schema Example
```json
{
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "$anchor": "product_title"
        },
        "skus": {
            "type": "array",
            "$anchor": "variant_sku"
        }
    }
}
```

## Advanced Features

### Array Handling

The remapper supports different array mapping strategies:

1. Direct mapping using anchors
2. Nested array mapping
3. Array transformation with filters

### Value Transformation

You can implement custom value transformers by extending the ValueNode class:

```python
from json_remapper.core.node import ValueNode

class TransformingValueNode(ValueNode):
    def get_value(self):
        # Apply custom transformation
        return transform_function(self.value)
```

### Schema Validation

The remapper validates both input and output schemas by default. You can customize validation behavior:

```python
mapper = ImportMapper(schema, validate_schema=False)  # Skip validation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.