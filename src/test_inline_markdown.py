import unittest
from textnode import TextNode, TextType
from inline_markdown import (split_nodes_delimiter, 
                             extract_markdown_images, 
                             extract_markdown_links, 
                             split_nodes_link, 
                             split_nodes_image)

class TestInlineMarkDown(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_italic_text(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), expected)

    def test_unmatched_delimiter(self):
        node = TextNode("This is an *italic text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_one_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_one_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(extract_markdown_links(text), expected)

    def test_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(extract_markdown_links(text), expected)


    def test_split_nodes_link_single(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode("Check [Google](https://google.com) and [GitHub](https://github.com)", TextType.TEXT)
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_image_single(self):
        node = TextNode("Here is an image ![alt text](https://image.com/image.png)", TextType.TEXT)
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://image.com/image.png"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode("Images: ![one](https://img1.com) and ![two](https://img2.com)", TextType.TEXT)
        expected = [
            TextNode("Images: ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "https://img1.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "https://img2.com"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This has no links.", TextType.TEXT)
        expected = [node]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("No images here.", TextType.TEXT)
        expected = [node]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_link_adjacent_links(self):
        node = TextNode("[Google](https://google.com)[GitHub](https://github.com)", TextType.TEXT)
        expected = [
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
        ]
        self.assertEqual(split_nodes_link([node]), expected)
    
    def test_split_nodes_image_adjacent_images(self):
        node = TextNode("![one](https://img1.com)![two](https://img2.com)", TextType.TEXT)
        expected = [
            TextNode("one", TextType.IMAGE, "https://img1.com"),
            TextNode("two", TextType.IMAGE, "https://img2.com"),
        ]
        self.assertEqual(split_nodes_image([node]), expected)
    


if __name__ == "__main__":
    unittest.main()
