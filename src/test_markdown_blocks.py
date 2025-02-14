import unittest

from markdown_blocks import (markdown_to_blocks,
                             block_to_block_type)


class TestMarkDownBlocks(unittest.TestCase):
    def test_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph."
        self.assertEqual(markdown_to_blocks(md), ["First paragraph.", "Second paragraph."])

    def test_leading_trailing_whitespace(self):
        md = "  \n\n  A paragraph with spaces.  \n\n"
        self.assertEqual(markdown_to_blocks(md), ["A paragraph with spaces."])

    def test_empty_lines_between_blocks(self):
        md = "First block.\n\n\n\nSecond block."
        self.assertEqual(markdown_to_blocks(md), ["First block.", "Second block."])

    def test_list_blocks(self):
        md = "* Item 1\n* Item 2\n\n* Item 3\n* Item 4"
        self.assertEqual(markdown_to_blocks(md), ["* Item 1\n* Item 2", "* Item 3\n* Item 4"])     

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), "heading")
    
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```code```"), "code")
    
    def test_quote(self):
        self.assertEqual(block_to_block_type("> Quote\n> Another line"), "quote")
    
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), "unordered_list")
    
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First\n2. Second"), "ordered_list")
        self.assertEqual(block_to_block_type("1. First\n2. Second\n3. Third"), "ordered_list")
    
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")
           
    def test_code_block_malformed(self):
        self.assertNotEqual(block_to_block_type("``\ncode\n``"), "code")
    
    def test_quote_malformed(self):
        self.assertNotEqual(block_to_block_type("> Quote\nNormal text"), "quote")

if __name__ == "__main__":
    unittest.main()
