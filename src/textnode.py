from enum import Enum
from htmlnode import LeafNode


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

    # Check if self is equal to other TextNode instance by comparing each attribute
    def __eq__(self, other):
        # Check each attribute
        if self.text != other.text: return False 
        if self.text_type != other.text_type: return False
        if self.url != other.url: return False 
        # All attributes were cheched and found the same
        return True                                         

    # Text representation of instance
    def __repr__(self): 
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        
def text_node_to_html_node(text_node):
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"text_to_text_node() called with invalid TextType {text_node.text_type}")
