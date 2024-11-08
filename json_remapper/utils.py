from typing import Any, Dict, List, Union
import json
from pathlib import Path


def load_json_file(path: Union[str, Path]) -> Dict[str, Any]:
    """Load JSON from a file"""
    with open(path) as f:
        return json.load(f)


def save_json_file(
    data: Dict[str, Any], path: Union[str, Path], indent: int = 2
) -> None:
    """Save JSON to a file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=indent)

def merge_schemas(schemas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge multiple schemas into one."""
    result = {}
    for schema in schemas:
        result.update(schema)
    return result