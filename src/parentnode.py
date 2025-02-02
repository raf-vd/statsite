from htmlnode import HTMLNode, HTMLTag
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag: raise ValueError("All parent nodes must have a tag")                       # Tag is require for a parentnode
        if not self.children: raise ValueError("All parent nodes must have a at least 1 child")    # Tag is require for a parentnode

        self.value = ""
        for node in self.children:                 # Because .to_html() is defined in LeafNode and ParentNode, this line will
            self.value += node.to_html()           # call ParentNode.to_html recursively when node contains a ParentNode
        return self.add_tag()                      # Create the actual HTML tag layout

    