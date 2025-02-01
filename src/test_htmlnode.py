import unittest

from htmlnode import HTMLNode, HTMLTag


class TestTextNode(unittest.TestCase):

    def test_value_if_no_children(self):
        node1 = HTMLNode(HTMLTag.H1, "value of header 1", None, None)
        # node1 = HTMLNode(HTMLTag.H1, None, None, None)
        self.assertIsNone(node1.children, "This testcase is only to be used for when parameter 'children' is 'None'")   # Will stop flow if a case is tested where children is not None
        self.assertIsNotNone(node1.value, "value is required when there are no children")

    def test_repr(self):
        node1 = HTMLNode(HTMLTag.H1, "value of header 1", None, None)
        self.assertEqual(node1.__repr__(), 
              f"  {{\n    HTMLNode\n\tTag: <h1>\n\tValue: value of header 1\n\tChildren: None\n\tProps: \n  }}")
        node1 = HTMLNode(HTMLTag.SA, "closing link tag", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node1.__repr__(), 
              f"  {{\n    HTMLNode\n\tTag: </a>\n\tValue: closing link tag\n\tChildren: None\n\tProps:  href=\"https://www.google.com\" target=\"_blank\"\n  }}")

    def test_props_to_html(self):
        node1 = HTMLNode(HTMLTag.H1, "value of header 1", None, None)
        self.assertEqual(node1.props_to_html(),"")
        node1 = HTMLNode(HTMLTag.SA, "closing link tag", None, {"href": "https://www.google.com","target": "_blank",})
        self.assertEqual(node1.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    

if __name__ == "__main__":
    unittest.main()



    