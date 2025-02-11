import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' in text '{node.text}'")
        
        #is_matching = False
        split_nodes = []

        for i, part in enumerate(parts):
            if part == "":
                continue
            
            if i % 2 != 0:
                split_nodes.append(TextNode(part, text_type))
            else:
                split_nodes.append(TextNode(part, TextType.TEXT))
            
        new_nodes.extend(split_nodes)
    
    return new_nodes

def extract_markdown_images(text):

    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches 

def extract_markdown_links(text):

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return matches
