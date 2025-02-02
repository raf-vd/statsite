import unittest

from leafnode import LeafNode
from htmlnode import HTMLTag

class TestLeafNode(unittest.TestCase):
# 
    def test_to_html(self):
        node1 = LeafNode(None, "plain text?", None)
        self.assertEqual(node1.to_html(),"plain text?")
        node1 = LeafNode(HTMLTag.H1, "This is a nice header (one), isn't it?", None)
        self.assertEqual(node1.to_html(),"<h1>This is a nice header (one), isn't it?</h1>")
        node1 = LeafNode(HTMLTag.B, "Some bold text perhaps?", None)
        self.assertEqual(node1.to_html(),"<b>Some bold text perhaps?</b>")
        node1 = LeafNode(HTMLTag.A, "click me!", {"href":"https://www.google.com"})
        self.assertEqual(node1.to_html(),'<a href="https://www.google.com">click me!</a>')
        node1 = LeafNode(HTMLTag.IMG, " ", {"src":"public/kitten.jpg","alt":"cutie"})
        self.assertEqual(node1.to_html(),'<img src="public/kitten.jpg" alt="cutie">')

if __name__ == "__main__":
    unittest.main()



    