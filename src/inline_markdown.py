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
        
        is_matching = False
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            
            if is_matching:
                new_nodes.append(TextNode(part, text_type))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
            
            is_matching = not is_matching
    
    return new_nodes
