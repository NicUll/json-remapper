import unittest
from json_remapper.schema import SchemaValidator
from json_remapper.exceptions import SchemaValidationError


class TestSchemaValidator(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "$anchor": "user_name", "minLength": 1},
                "age": {"type": "integer", "$anchor": "user_age", "minimum": 0},
            },
            "required": ["name"],
        }
        self.validator = SchemaValidator(self.schema)

    def test_valid_data(self):
        data = {"name": "John Doe", "age": 30}
        try:
            self.validator.validate(data)
        except SchemaValidationError:
            self.fail("Validation raised SchemaValidationError unexpectedly!")

    def test_invalid_data(self):
        data = {"name": "", "age": -1}  # Invalid: empty string  # Invalid: negative age
        with self.assertRaises(SchemaValidationError) as context:
            self.validator.validate(data)

        self.assertTrue(len(context.exception.errors["errors"]) == 2)

    def test_anchor_paths(self):
        paths = self.validator.get_anchor_paths("user_name")
        self.assertTrue(len(paths) > 0)
        self.assertIn("properties.name", paths[0])
        
if __name__ == "__main__":
    unittest.main()