from htmlnode import HTMLNode, HTMLTag

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def add_basic_tag(self):
        return f"{self.tag.value}{self.value}{self.tag.value.replace("<","</")}"
    
    def add_link_tag(self):
        w= self.props_to_html()
        x = self.tag.value.replace(">", w + ">")
        y = x + self.value
        z = y + self.tag.value.replace("<","</")
        return z

    def to_html(self):
        if not self.value: raise ValueError("All leaf nodes must have a value")     # value is requiref for a leafnode
        if not self.tag: return self.value                                          # empty tag => return value in plain text

        match self.tag:
            case _ if self.tag in [HTMLTag.H1, HTMLTag.H2, HTMLTag.H3, HTMLTag.H4, HTMLTag.H5, HTMLTag.H6,
                                   HTMLTag.P, 
                                   HTMLTag.B, HTMLTag.I, HTMLTag.U]: return self.add_basic_tag()
            case HTMLTag.A: return self.add_link_tag()
            case _: raise ValueError()
