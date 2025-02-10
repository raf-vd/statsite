import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:                             # Only split TextType.TEXT nodes (no bold, image, ...)
            new_nodes.append(node)                                      # Add non TextType.TEXT nodes directlt to new_nodes
            continue                                                    # Next node

        parts= node.text.split(delimiter, 2)                            # Split old node into 3 parts
        if len(parts) == 2:                                             # No closing tag found, raise error
            raise Exception(f"Invallid markdown: {node.text}")
        if len(parts) == 1:
            if parts[0]:                                            
                new_nodes.append(TextNode(parts[0], TextType.TEXT))     # Delimiter not found, return plain TextNode
                continue                                            

        if parts[0]:
            new_nodes.append(TextNode(parts[0], TextType.TEXT))         # Add first part as regular text TextNode
        if parts[1]:
            new_nodes.append(TextNode(parts[1], text_type))             # Add second part as requested type TextNode
        if parts[2]:                                                    # Call function recursively untill end of text is reached
            new_nodes.extend(split_nodes_delimiter([TextNode(parts[2], TextType.TEXT)], delimiter, text_type))

    return new_nodes                                                    # Return the new list of nodes

def __split_nodes_link_or_image(old_nodes, text_type):
    new_nodes = []
    for node in old_nodes:

        found = extract_markdown_links_or_images(node.text, text_type)      # Look for links
        if not found:                                                    
            new_nodes.append(node)                                          # If no links found, return original TextNode
            continue
        
        search_in = node.text                                               # Copy node text
        for item in found:
            image = "!" if text_type == TextType.IMAGE else ""
            pattern = f"{image}[{item[0]}]({item[1]})"
            parts = search_in.split(pattern, 1)                             # Split node text to find search text
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))         # Add first part as regular text TextNode
            new_nodes.append(TextNode(item[0], text_type, item[1]))     # Add the found item as TextNode
            if parts[1]:
                search_in = search_in.replace(f"{parts[0]}{pattern}", "")   # If there was a trailing part, search that too
        if parts[1]:
            new_nodes.append(TextNode(parts[1], TextType.TEXT))             # Add the last trailing part if present
    return new_nodes

def split_nodes_link(old_nodes):
    return __split_nodes_link_or_image(old_nodes, TextType.LINK)

def split_nodes_image(old_nodes):
    return __split_nodes_link_or_image(old_nodes, TextType.IMAGE)

def extract_markdown_links_or_images(text, text_type):
    if text_type == TextType.IMAGE:
        return extract_markdown_images(text)
    else:
        return extract_markdown_links(text)

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)" # image
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)" # link
    return re.findall(pattern, text)

def text_to_textnodes(text):
    nodes = []
    nodes.append(TextNode(text, TextType.TEXT))
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
# nodes = text_to_text_nodes(text)
# for node in nodes:
#     print(node)