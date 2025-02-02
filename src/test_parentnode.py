import unittest

from parentnode import ParentNode
from htmlnode import HTMLTag
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    
    # Non-nested tests
    def test_to_html_1_basic_child(self):
        node1 = ParentNode(
                HTMLTag.P,
                [LeafNode(HTMLTag.H1, "Hoe werken headertags eigenlijk?"),],
            ) 
        should_be = "<p><h1>Hoe werken headertags eigenlijk?</h1></p>"
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_2_basic_children(self):
        node1 = ParentNode(
                HTMLTag.P,
                [
                LeafNode(HTMLTag.H1, "Hoe werken headertags eigenlijk?"),
                LeafNode(HTMLTag.U, "underlined tekst"),
                ],
            ) 
        should_be = "<p><h1>Hoe werken headertags eigenlijk?</h1><u>underlined tekst</u></p>"
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_6_basic_children(self):
        node1 = ParentNode(
                HTMLTag.P,
                [
                LeafNode(HTMLTag.H1, "head1"),
                LeafNode(HTMLTag.U, "u 1"),
                LeafNode(HTMLTag.I, "i 1"),
                LeafNode(HTMLTag.U, "u 2"),
                LeafNode(HTMLTag.B, "b 1"),
                LeafNode(HTMLTag.U, "u 3"),
                ],
            ) 
        should_be = "<p><h1>head1</h1><u>u 1</u><i>i 1</i><u>u 2</u><b>b 1</b><u>u 3</u></p>"
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_0_children(self):

        node1 = ParentNode(HTMLTag.P, [],)      # No children SHOULD raise a ValueError 
        with self.assertRaises(ValueError):     # This code will cause a fail if it does not
            node1.to_html()
        
        node1 = ParentNode(HTMLTag.P, None,)    # No children SHOULD raise a ValueError 
        with self.assertRaises(ValueError):     #This code will cause a fail if it does not
            node1.to_html()

    def test_to_html_1_link_child(self):
        node1 = ParentNode(
                HTMLTag.P,
                [LeafNode(HTMLTag.A, "clickbait", {"href": "https://www.google.com"}),],
            ) 
        should_be = '<p><a href="https://www.google.com">clickbait</a></p>'
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_2_link_children(self):
        node1 = ParentNode(
                HTMLTag.P,
                [
                LeafNode(HTMLTag.A, "clickbait", {"href": "https://www.google.com"}),
                LeafNode(HTMLTag.A, "newspaper in BE", {"href": "https://www.hln.be"}),
                ],
            ) 
        should_be = '<p><a href="https://www.google.com">clickbait</a><a href="https://www.hln.be">newspaper in BE</a></p>'
        self.assertEqual(node1.to_html(),should_be)

    # Nested tests
    def test_to_html_1b_1P3_1b_child(self):
        node_n1 = ParentNode(
                  HTMLTag.P,
                  [
                  LeafNode(None, "Gogo italic!: "),
                  LeafNode(HTMLTag.I, "inner italic test"),
                  LeafNode(None, " Italic no more!"),
                  ],
                ) 
        node1 = ParentNode(
                HTMLTag.P,
                [
                LeafNode(HTMLTag.H1, "Hoe werken headertags eigenlijk?"),
                node_n1,
                LeafNode(HTMLTag.B, "bold"),
                ],
            ) 
        should_be = "<p><h1>Hoe werken headertags eigenlijk?</h1><p>Gogo italic!: <i>inner italic test</i> Italic no more!</p><b>bold</b></p>"
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_1P1_child(self):
        node_n1 = ParentNode(
                  HTMLTag.P,
                  [
                  LeafNode(HTMLTag.I, "inner italic test"),
                  ],
                ) 
        node1 = ParentNode(
                HTMLTag.P,
                [
                node_n1,
                ],
            ) 
        should_be = "<p><p><i>inner italic test</i></p></p>"
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_2P2_child(self):
        node_n1 = ParentNode(
                  HTMLTag.P,
                  [
                  LeafNode(HTMLTag.H1, "head1"),
                  LeafNode(HTMLTag.U, "u 1"),
                  ],
                ) 
        node_n2 = ParentNode(
                  HTMLTag.P,
                  [
                  LeafNode(HTMLTag.H2, "head2"),
                  LeafNode(None, "basic text"),
                  ],
                ) 
        node1 = ParentNode(
                HTMLTag.P,
                [node_n1, node_n2,],
            ) 
        should_be = "<p><p><h1>head1</h1><u>u 1</u></p><p><h2>head2</h2>basic text</p></p>"
        self.assertEqual(node1.to_html(),should_be)

    def test_to_html_multi_nest_child(self):
        node_nn1 = ParentNode(HTMLTag.B, [LeafNode(None, "bold double nested")], )

        node_n1 = ParentNode(
                  HTMLTag.P,
                  [
                  node_nn1,
                  LeafNode(HTMLTag.H1, "head1"),
                  LeafNode(HTMLTag.U, "u 1"),
                  ],
                ) 
        node_n2 = ParentNode(
                  HTMLTag.P,
                  [
                  LeafNode(HTMLTag.H2, "head2"),
                  node_nn1,
                  LeafNode(None, "basic text"),
                  ],
                ) 
        node1 = ParentNode(
                HTMLTag.P,
                [node_n1, node_n2,],
            ) 
        should_be = "<p><p><b>bold double nested</b><h1>head1</h1><u>u 1</u></p><p><h2>head2</h2><b>bold double nested</b>basic text</p></p>"
        self.assertEqual(node1.to_html(),should_be)


if __name__ == "__main__":
    unittest.main()
