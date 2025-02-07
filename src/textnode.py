import re
from enum import Enum
from leafnode import LeafNode
from htmlnode import HTMLTag

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text != other.text:  return False
        if self.text_type != other.text_type: return False
        if self.url != other.url: return False
        return True
    
    def __repr__(self):
        return f'TextNode(text="{self.text}", text_type="{self.text_type.value}", url="{self.url}")'
        # return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if not text_node.text_type in TextType:
        raise Exception("This is not a valid TextNode type")
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode(HTMLTag.B, text_node.text)
        case TextType.ITALIC:
            return LeafNode(HTMLTag.I, text_node.text)
        case TextType.CODE:
            return LeafNode(HTMLTag.C, text_node.text)
        case TextType.LINK:
            return LeafNode(HTMLTag.A, text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(HTMLTag.IMG, "", {"src": text_node.url,"alt": text_node.text})
        case _:
            raise Exception("This is not a convertible TextNode type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes: return []

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node)            
        else:
            parts = node.text.split(delimiter, 2)
            if len(parts) == 1:
                new_nodes.append(node)
            elif len(parts) == 2:
                raise Exception("The node doesn't contain a valid Markdown syntax")
            else:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                new_nodes.append(TextNode(parts[1], text_type))
                new_nodes.extend(split_nodes_delimiter([TextNode(parts[2], TextType.TEXT)], delimiter, text_type))
                # new_nodes.append(TextNode(parts[2], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes, img=""):
    new_nodes = []                                                                  # Create empty list to add to
    for node in old_nodes:                                                          # Loop across all input nodes
        if node.text_type != TextType.TEXT:                                         # If not a TEXT noden just add to list
            new_nodes.append(node)
        else:
            if img: links = extract_markdown_images(node.text)                      # Extract links from the node
            else: links = extract_markdown_links(node.text)                         # Extract links from the node
            for link in links:                                                      # Loop all found links
                parts = node.text.split(f"{img}[{link[0]}]({link[1]})", 1)          # Find whatever is before the link
                if parts[0] != "":                                              
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))             # Append whatever is before link to new list
                    node.text = node.text.replace(f"{parts[0]}", "")                # Remove the just added text from the original node text                    
                new_nodes.append(TextNode(link[0], TextType.IMAGE if img else TextType.LINK, link[1])) # Append the image/link itself as a (LINK) node
                node.text = node.text.replace(f"{img}[{link[0]}]({link[1]})", "")   # Remove the just added link from the original node text
            if node.text != '':                                                     # Don't do anything if nothing after final link
                new_nodes.append(TextNode(node.text, TextType.TEXT))                # Apend the text after final link 
    return new_nodes                                                                # Return the list

def split_nodes_image(old_nodes):                                                   # Call code for link with optional parameter (! to indicate image)
    return split_nodes_link(old_nodes, "!")                                         # Return the list

def text_to_textnodes(text):
    nodes = []
    nodes.append(TextNode(text, TextType.TEXT))
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
