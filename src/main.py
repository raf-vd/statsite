from textnode import TextNode, TextType
from htmlnode import HTMLNode, HTMLTag
from leafnode import LeafNode
from parentnode import ParentNode

def main():
    # node1 = LeafNode(None, "plain text?", None)
    # node1 = LeafNode(HTMLTag.H1, "This is a nice header (one), isn't it?", None)
    # node1 = LeafNode(HTMLTag.H5, "This is a nice header FIVE, isn't it?", None)
    # node1 = LeafNode(HTMLTag.B, "Some bold text perhaps?", None)
    # node1 = LeafNode(HTMLTag.A, "click me!", {"href": "https://www.google.com"})
    node_n1 = ParentNode(HTMLTag.P, [], ) 
    node1 = ParentNode(HTMLTag.P, [node_n1,],) 
 
    print(node1)
    print(node1.to_html())


main()

