from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT =   "Bold text"
    ITALIC_TEXT = "Italic text"
    CODE_TEXT =   "Code text"
    LINKS =       "Links"
    IMAGES =      "Images"

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
