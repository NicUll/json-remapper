import unittest
from json_remapper import JSONMapper, ImportMapper, ExportMapper
from json_remapper.exceptions import SchemaValidationError


class TestJSONMapper(unittest.TestCase):
    def setUp(self):
        self.input_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "$anchor": "user_name"},
                "age": {"type": "integer", "$anchor": "user_age"},
            },
            "required": ["name"],
        }

        self.output_schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "fullName": {"type": "string", "$anchor": "user_name"},
                        "years": {"type": "integer", "$anchor": "user_age"},
                    },
                }
            },
        }

    def test_basic_mapping(self):
        input_data = {"name": "John Doe", "age": 30}

        import_mapper = ImportMapper(self.input_schema)
        export_mapper = ExportMapper(self.output_schema, import_mapper)

        intermediate = import_mapper.map(input_data)
        result = export_mapper.map(intermediate)

        expected = {"user": {"fullName": "John Doe", "years": 30}}

        self.assertEqual(result, expected)

    def test_validation_error(self):
        input_data = {
            "age": 30 # Missing required 'name' field
        }
        
        import_mapper = ImportMapper(self.input_schema)
        
        with self.assertRaises(SchemaValidationError):
            import_mapper.map(input_data)