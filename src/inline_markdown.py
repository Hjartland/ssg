import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
        
        
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter '{delimiter}' in text '{node.text}'")
        
        parts = node.text.split(delimiter)
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

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        text = node.text
        last_index = 0
        for match in matches:
            link_text, link_url = match
            start_index = text.find(f'[{link_text}]({link_url})', last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(text[last_index:start_index], TextType.TEXT))
            
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            last_index = start_index + len(f'[{link_text}]({link_url})')
        
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        text = node.text
        last_index = 0
        for match in matches:
            alt_text, image_url = match
            start_index = text.find(f'![{alt_text}]({image_url})', last_index)
            if start_index > last_index:
                new_nodes.append(TextNode(text[last_index:start_index], TextType.TEXT))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            last_index = start_index + len(f'![{alt_text}]({image_url})')
        
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
 
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    
    return nodes