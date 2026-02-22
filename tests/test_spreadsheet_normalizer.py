import unittest

from spreadsheet_normalizer import normalize_spreadsheet_schema


class NormalizeSpreadsheetSchemaTests(unittest.TestCase):
    def test_normalizes_headers_to_snake_case(self) -> None:
        mappings = normalize_spreadsheet_schema(["First Name", "E-mail Address"])
        self.assertEqual([m.normalized_name for m in mappings], ["first_name", "e_mail_address"])

    def test_generates_defaults_for_empty_headers(self) -> None:
        mappings = normalize_spreadsheet_schema(["", "!!!", "Name"])
        self.assertEqual([m.normalized_name for m in mappings], ["column_1", "column_2", "name"])

    def test_deduplicates_duplicate_names(self) -> None:
        mappings = normalize_spreadsheet_schema(["Name", "name", "NAME"])
        self.assertEqual([m.normalized_name for m in mappings], ["name", "name_2", "name_3"])

    def test_handles_unicode_characters(self) -> None:
        mappings = normalize_spreadsheet_schema(["Café", "naïve score"])
        self.assertEqual([m.normalized_name for m in mappings], ["cafe", "naive_score"])


if __name__ == "__main__":
    unittest.main()
