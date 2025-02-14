import unittest
from htmlnode import ParentNode
from markdown_to_html_converter import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_heading(self):
        markdown = "# Heading 1"
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<h1>', html_node.to_html())

    def test_paragraph(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<p>', html_node.to_html())

    def test_code_block(self):
        markdown = "```code block```"
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<pre>', html_node.to_html())

    def test_quote_block(self):
        markdown = "> This is a quote."
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<blockquote>', html_node.to_html())

    def test_unordered_list(self):
        markdown = "* item 1\n* item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<ul>', html_node.to_html())

    def test_ordered_list(self):
        markdown = "1. item 1\n2. item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<ol>', html_node.to_html())

    def test_inline_bold(self):
        markdown = "**bold text**"
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<b>', html_node.to_html())

    def test_inline_italic(self):
        markdown = "*italic text*"
        html_node = markdown_to_html_node(markdown)
        self.assertIn('<i>', html_node.to_html())

if __name__ == "__main__":
    unittest.main()
