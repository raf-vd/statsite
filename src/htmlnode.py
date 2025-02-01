from enum import Enum

class HTMLTag(Enum):
    H1, H2, H3, H4, H5, H6 = tuple([f"<h{x}>" for x in range(1,7) ])        # header opening tags
    P= "<p>"                                                                # paragrap tag
    B, I, U = "<b>", "<i>", "<u>"                                           # bold, italic, underline
    A = "<a>"                                                               # link

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

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

# hn=node1 = HTMLNode(HTMLTag.SA, "closing link tag", None, {"href": "https://www.google.com","target": "_blank",})
# print(hn)
# print(f"  {{\n    HTMLNode\n\tTag: </a>\n\tValue: value of header 1\n\tChildren: None\n\tProps:  href=\"https://www.google.com\" target=\"_blank\"\n  }}")
# print(f"  {{\n    HTMLNode\n\tTag: <h1>\n\tValue: value of header 1\n\tChildren: None\n\tProps: \n  }}")
# hn=HTMLNode(HTMLTag.H1, "myTagValue", children=None, props={"href": "https://www.google.com","target": "_blank",})
# node1 = HTMLNode(HTMLTag.H1, "value of header 1", None, None)
# print(hn)
# dict = {
#     "href": "https://www.google.com",
#     "target": "_blank",
#     }
# print('***')
# for key in dict:
#     print(f"{key}={dict[key]}")
