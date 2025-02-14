import re

def markdown_to_blocks(markdown):
    
    blocks = re.split(r'\n{2,}', markdown.strip())
    cleaned_blocks = [block.strip() for block in blocks if block.strip()]
    return cleaned_blocks

def block_to_block_type(block):
    
    if re.match(r'^#{1,6} ', block):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif all(line.startswith(">") for line in block.split("\n")):
        return "quote"
    elif all(re.match(r'^[\*-] ', line) for line in block.split("\n")):
        return "unordered_list"
    elif all(re.match(r'^[1-9][0-9]*\. ', line) for line in block.split("\n")):
        return "ordered_list"
    else:
        return "paragraph"