from textnode import TextNode, TextType
from htmlnode import HTMLNode, HTMLTag
from leafnode import LeafNode

def main():
    # node1 = LeafNode(None, "plain text?", None)
    # node1 = LeafNode(HTMLTag.H1, "This is a nice header (one), isn't it?", None)
    # node1 = LeafNode(HTMLTag.H5, "This is a nice header FIVE, isn't it?", None)
    # node1 = LeafNode(HTMLTag.B, "Some bold text perhaps?", None)
    node1 = LeafNode(HTMLTag.A, "click me!", {"href": "https://www.google.com"})
    print(node1.to_html())


main()

