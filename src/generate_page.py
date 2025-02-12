import os
import re
import pathlib
# import shutil
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    pattern = r"(?<!.)# (.+)"                       # Define pattern (find # followed by any text not preceded by anything )
    title = re.findall(pattern, markdown)           # Grab (all) matches
    if not title:                                   # [] = False
        raise Exception("No title in markdown")     
    return title[0]                                 # Return first found

def read_file(file):
    openfile = open(file, "r")
    content = openfile.read()
    openfile.close()
    return content

def write_file(dest_path, content):
    # check for dependancies in the md (images, folders)
    openfile = open(dest_path, "w")
    openfile.write(content)
    openfile.close()    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_path_content = read_file(from_path)
    template_path_content = read_file(template_path)

    html_node_from_path = markdown_to_html_node(from_path_content)
    html_from_path = html_node_from_path.to_html()

    title = extract_title(from_path_content)
    des_path_content = template_path_content.replace("{{ Title }}", title)
    des_path_content = des_path_content.replace("{{ Content }}", html_from_path)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    write_file(dest_path, des_path_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):                                                       # List & loop files & folders
        source = os.path.join(dir_path_content, filename)                                               
        target = os.path.join(dest_dir_path, filename.replace(".md",".html"))
        if os.path.isfile(source):                                                                      # Generate page from file
            generate_page(source, template_path,target)
        else:                                                                                           
            generate_pages_recursive(source, template_path, os.path.join(dest_dir_path, filename))      # For folder: recursively call function
