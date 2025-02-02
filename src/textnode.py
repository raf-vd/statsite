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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


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
