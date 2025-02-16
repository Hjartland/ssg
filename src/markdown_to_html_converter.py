import re
from htmlnode import ParentNode
from markdown_blocks import markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def handle_heading(block):
    level = block.count('#')
    text = block[level+1:]
    return ParentNode(f"h{level}", text_to_children(text))

def handle_paragraph(block):
    return ParentNode("p", text_to_children(block))

def handle_code(block):
    code_content = block.strip('`')
    return ParentNode("pre", [ParentNode("code", text_to_children(code_content))])

def handle_quote(block):
    lines = [line.lstrip('> ') for line in block.split('\n')]
    return ParentNode("blockquote", text_to_children(" ".join(lines)))

def handle_unordered_list(block):
    #items = [line.lstrip('*- ') for line in block.split('\n')]
    items = [re.sub(r'^[\*-] ', '', line) for line in block.split('\n')]
    #print("Items after stripping:", items)  # Debug line
    children = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", children)

def handle_ordered_list(block):
    items = [re.sub(r'^\d+\. ', '', line) for line in block.split('\n')]
    children = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "heading":
        return handle_heading(block)
    elif block_type == "paragraph":
        return handle_paragraph(block)
    elif block_type == "code":
        return handle_code(block)
    elif block_type == "quote":
        return handle_quote(block)
    elif block_type == "unordered_list":
        return handle_unordered_list(block)
    elif block_type == "ordered_list":
        return handle_ordered_list(block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
