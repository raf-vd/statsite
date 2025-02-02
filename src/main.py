from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, HTMLTag
from leafnode import LeafNode
from parentnode import ParentNode


def main():
    # node1 = LeafNode(None, "plain text?", None)
    # node1 = LeafNode(HTMLTag.H1, "This is a nice header (one), isn't it?", None)
    # node1 = LeafNode(HTMLTag.H5, "This is a nice header FIVE, isn't it?", None)
    # node1 = LeafNode(HTMLTag.B, "Some bold text perhaps?", None)
    # node1 = LeafNode(HTMLTag.A, "click me!", {"href": "https://www.google.com"})
    # node1 = LeafNode(HTMLTag.IMG, " ", {"src":"public/kitten.jpg","alt":"cutie"})
    
    # tn = TextNode("just some text", TextType.TEXT)
    # tn = TextNode("just some bold text", TextType.BOLD)
    # tn = TextNode("just some italic text", TextType.ITALIC)
    # tn = TextNode('print("just some code")', TextType.CODE)
    # tn = TextNode("clickbait", TextType.LINK, "https://www.hln.be")
    tn = TextNode("cutie", TextType.IMAGE, "image/kitten.jpg")
    ln= text_node_to_html_node(tn)
    print(ln.to_html())

main()

