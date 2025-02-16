import os
from markdown_to_html_converter import markdown_to_html_node
from extract_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown_content = file.read()

    with open(template_path) as file:
        template_content = file.read()
    
    html_string = markdown_to_html_node(markdown_content).to_html()
    page_title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", page_title)
    template_content = template_content.replace("{{ Content }}", html_string)

    parent_dir = os.path.dirname(dest_path)
    if parent_dir and not os.path.exists(parent_dir):  # Ensure parent directory exists and is valid
        
        os.makedirs(parent_dir)

    formatted_content = template_content.replace('><', '>\n<')

    with open(dest_path, "w") as file:
        file.write(formatted_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(os.listdir(dir_path_content))  
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, content)
        if os.path.isfile(content_path) and content.endswith('.md'):
            rel_path = os.path.relpath(content_path, dir_path_content)
            rel_path = os.path.splitext(rel_path)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, rel_path) 
            generate_page(content_path, template_path, dest_path)

        elif os.path.isdir(content_path):
            
            new_dest_dir = os.path.join(dest_dir_path, content)
            generate_pages_recursive(content_path, template_path, new_dest_dir)