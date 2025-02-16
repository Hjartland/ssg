import unittest

from extract_markdown import extract_title

class TestExtractMarkdown(unittest.TestCase):

    def test_single_h1(self):
        markdown = "# This is a title"
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_multiple_h1(self):
        markdown = """# First title
# Second title"""
        self.assertEqual(extract_title(markdown), "First title")

    def test_no_h1(self):
        markdown = "## Subtitle\nSome content"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_h1_with_whitespace(self):
        markdown = "#     Title with spaces    "
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_h1_among_other_text(self):
        markdown = """
Some introduction text
# Main Title
More content here
        """
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_only_h1(self):
        markdown = "# Only Title"
        self.assertEqual(extract_title(markdown), "Only Title")

    def test_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_no_lines(self):
        markdown = "\n\n"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")

    def test_h1_with_special_characters(self):
        markdown = "# Title with @#$%^&*"
        self.assertEqual(extract_title(markdown), "Title with @#$%^&*")

if __name__ == "__main__":
    unittest.main()
