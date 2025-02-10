from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance (other, TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url ==other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url and text_node.text:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        elif not text_node.url:
            raise ValueError ("URL  is missing")
        raise ValueError ("Text is missing")
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url:
            alt_text = text_node.text  # Since the first argument is the alt text
            return LeafNode("img", "", {"src": text_node.url, "alt": alt_text})
        raise ValueError("Image URL is missing")
    else:
        raise ValueError("Invalid TextType for text node.")