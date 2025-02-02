from enum import Enum

class HTMLTag(Enum):
    A = "<a>"                                                               # link
    B, I, U = "<b>", "<i>", "<u>"                                           # bold, italic, underline
    C = "<code>"                                                            # code
    H1, H2, H3, H4, H5, H6 = tuple([f"<h{x}>" for x in range(1,7) ])        # header opening tags
    IMG = "<img>"                                                           # image
    P= "<p>"                                                                # paragrap tag

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def add_tag(self):
        match self.tag:
            case _ if self.tag in [HTMLTag.H1, HTMLTag.H2, HTMLTag.H3, HTMLTag.H4, HTMLTag.H5, HTMLTag.H6,
                                   HTMLTag.P, HTMLTag.C,
                                   HTMLTag.B, HTMLTag.I, HTMLTag.U]: return self.add_basic_tag()
            case HTMLTag.A: return self.add_link_tag()
            case HTMLTag.IMG: return self.add_image_tag()
            case _: raise ValueError(f"{self.tag} is not a constant in the HTMLTag Enum")

    def add_basic_tag(self):
        return f"{self.tag.value}{self.value}{self.tag.value.replace("<","</")}"

    def add_link_tag(self):
        return self.tag.value.replace(">", self.props_to_html() + ">") + self.value + self.tag.value.replace("<","</")
    
    def add_image_tag(self):
        return self.tag.value.replace(">", self.props_to_html() + ">")
        
    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")

    def props_to_html(self):
        out = ""
        if self.props:
            for prop in self.props:
                out += f' {prop}="{self.props[prop]}"'
        return out
    
    def __repr__(self):
        out =[]
        out.append("  {")
        out.append("    HTMLNode")
        out.append(f"\tTag: {self.tag.value}")
        out.append(f"\tValue: {self.value}")
        out.append(f"\tChildren: {self.children}")
        out.append(f"\tProps: {self.props_to_html()}")
        out.append("  }")
        return "\n".join(out)

