import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an image text node", TextType.IMAGES, "url/of/image.jpg")
        self.assertEqual(node1.__repr__(), "TextNode(This is a text node, Bold text, None)")
        self.assertEqual(node2.__repr__(), "TextNode(This is an image text node, Images, url/of/image.jpg)")

    def test_neq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL, None)
        self.assertNotEqual(node1, node2)
        
    def test_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertIn(node1.text_type, TextType)

if __name__ == "__main__":
    unittest.main()
