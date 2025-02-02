from htmlnode import HTMLNode, HTMLTag

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None: raise ValueError("Leaf node value cannot be None")   # value is require for a leafnode
        if not self.tag: return self.value                                          # empty tag => return value in plain text
        return self.add_tag()                                                       # Create the actual HTML tag layout
