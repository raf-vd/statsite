class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("HTMLNode: to_html() is to be implemented in derived classes")

    # Return props dict in a HTML string
    def props_to_html(self):
        prop_html = ""
        if self.props is not None:
            for prop in self.props:
                prop_html += f' {prop}="{self.props[prop]}"'
        return prop_html
    
    # Text representation of instance
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)   # Call HTMLNode constructor without children

    # Return leaf in a HTML string
    def to_html(self):
        if self.value is None:                      
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:                                        # If the node has no tag
            return self.value                                       # just return the raw value
        # Return value with tag added and props into opening tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    # Text representation of instance
    def __repr__(self):
        # return f"LeafNode({self.tag}, {self.value}, {self.props})\t(From: {super().__repr__()})"
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A parent node requires a tag")
        if self.children is None:
            raise ValueError("A parent node must have at least 1 child")
        
        # Create a HTML string containing the full tree of Parent+Children nodes using recursion
        html = f"<{self.tag}{self.props_to_html()}>"        # Open ParentNode tag
        for node in self.children:                          # Loop all children
            html += node.to_html()                          # Call .to_html() recursively when node is a ParenNode, else call it on LeafNode
        html += f"</{self.tag}>"                            # Close ParentNode tag

        # Return the full HTML representation of the node
        return html

    def __repr__(self):
        # return f"ParentNode({self.tag}, children: {self.children}, {self.props})\t(From: {super().__repr__()})"
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
