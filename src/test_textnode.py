import unittest

from textnode import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_repr(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an image text node", TextType.IMAGE, "url/of/image.jpg")
        self.assertEqual(node1.__repr__(), 'TextNode(text="This is a text node", text_type="bold", url="None")')
        self.assertEqual(node2.__repr__(), 'TextNode(text="This is an image text node", text_type="image", url="url/of/image.jpg")')

    def test_neq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertNotEqual(node1, node2)
        
    def test_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertIn(node1.text_type, TextType)

    def test_split_nodes_delimiter(self):
        # 1 #
        nodes = []
        nodes.append(TextNode("`code block`", TextType.TEXT))
        self.assertListEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), 
                             [
                                TextNode(text="", text_type=TextType.TEXT),
                                TextNode(text="code block", text_type=TextType.CODE),
                                TextNode(text="", text_type=TextType.TEXT),
                             ])
        # 2 #
        nodes = []
        nodes.append(TextNode("This is text with a `code block` word", TextType.TEXT))
        self.assertListEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), 
                             [
                                TextNode(text="This is text with a ", text_type=TextType.TEXT),
                                TextNode(text="code block", text_type=TextType.CODE),
                                TextNode(text=" word", text_type=TextType.TEXT),
                             ])
        # 3 #
        nodes = []
        nodes.append(TextNode("Split **bold** word don't split *italic* just yet", TextType.TEXT))
        self.assertListEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), 
                             [
                                TextNode(text="Split ", text_type=TextType.TEXT),
                                TextNode(text="bold", text_type=TextType.BOLD),
                                TextNode(text=" word don't split *italic* just yet", text_type=TextType.TEXT),
                             ])
        # 4 #
        nodes = []
        nodes.append(TextNode("Split **bold** word and split *italic*", TextType.TEXT))
        self.assertListEqual(split_nodes_delimiter(
                                split_nodes_delimiter(nodes, "**", TextType.BOLD), 
                                "*", TextType.ITALIC),
                             [
                                TextNode(text="Split ", text_type=TextType.TEXT),
                                TextNode(text="bold", text_type=TextType.BOLD),
                                TextNode(text=" word and split ", text_type=TextType.TEXT),
                                TextNode(text="italic", text_type=TextType.ITALIC),
                                TextNode(text="", text_type=TextType.TEXT),
                             ])
        # 5 #
        nodes = []
        nodes.append(TextNode("Should simply pass unchanged", TextType.BOLD))
        self.assertListEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), 
                             [
                                TextNode(text="Should simply pass unchanged", text_type=TextType.BOLD),
                             ])

        # 5 #
        nodes = []
        nodes.append(TextNode("Should raise **an error due to missing closing bold delimiter", TextType.TEXT))
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

        # 6 # Multi occurance
        nodes = []
        nodes.append(TextNode("This is text with a **bold** word an another 2 **bold words**. **SURELY** I aplied recursion here ;-)", TextType.TEXT))
        self.assertListEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), 
                             [
                                TextNode(text="This is text with a ", text_type=TextType.TEXT),
                                TextNode(text="bold", text_type=TextType.BOLD),
                                TextNode(text=" word an another 2 ", text_type=TextType.TEXT),
                                TextNode(text="bold words", text_type=TextType.BOLD),
                                TextNode(text=". ", text_type=TextType.TEXT),
                                TextNode(text="SURELY", text_type=TextType.BOLD),
                                TextNode(text=" I aplied recursion here ;-)", text_type=TextType.TEXT),
                             ])
        
    def test_extract_markdown_images(self):
        images = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(extract_markdown_images(images), 
                            [
                                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), 
                                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
                            ])

    def test_extract_markdown_links(self):
        links = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(extract_markdown_links(links), 
                            [
                                ('to boot dev', 'https://www.boot.dev'), 
                                ('to youtube', 'https://www.youtube.com/@bootdotdev')
                            ])

    def test_split_nodes_link(self):
        # 1 #
        nodes = []
        nodes.append(TextNode("[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT))
        self.assertListEqual(split_nodes_link(nodes), 
                             [
                                TextNode(text="to youtube", text_type=TextType.LINK, url="https://www.youtube.com/@bootdotdev")
                             ])        
        
        # 2 #
        nodes = []
        nodes.append(TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) followed by some final text", TextType.TEXT))
        self.assertListEqual(split_nodes_link(nodes), 
                            [
                                TextNode(text="This is text with a link ", text_type=TextType.TEXT, url=None), 
                                TextNode(text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"), 
                                TextNode(text=" and ", text_type=TextType.TEXT, url=None), 
                                TextNode(text="to youtube", text_type=TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
                                TextNode(text=" followed by some final text", text_type=TextType.TEXT, url=None), 
                            ])        
        
        # 3 #
        nodes = []
        nodes.append(TextNode("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT))
        self.assertListEqual(split_nodes_link(nodes), 
                             [
                                TextNode(text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"), 
                                TextNode(text="to youtube", text_type=TextType.LINK, url="https://www.youtube.com/@bootdotdev")
                             ])        
        
    def test_split_nodes_image(self):
            # 1 #
            nodes = []
            nodes.append(TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT))
            self.assertListEqual(split_nodes_image(nodes), 
                                [
                                    TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif")
                                ])        
        
            # 2 #
            nodes = []
            nodes.append(TextNode("This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) followed by some final text", TextType.TEXT))
            self.assertListEqual(split_nodes_image(nodes), 
                                [
                                    TextNode(text="This is text with an image ", text_type=TextType.TEXT, url=None), 
                                    TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
                                    TextNode(text=" and ", text_type=TextType.TEXT, url=None), 
                                    TextNode(text="obi wan", text_type=TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"),
                                    TextNode(text=" followed by some final text", text_type=TextType.TEXT, url=None), 
                                ])        
            
            # 3 #
            nodes = []
            nodes.append(TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT))
            self.assertListEqual(split_nodes_image(nodes), 
                                [
                                    TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"),
                                    TextNode(text="obi wan", text_type=TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg")
                                ])               

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(text_to_textnodes(text), 
                             [
                            TextNode(text="This is ", text_type=TextType.TEXT, url=None),
                            TextNode(text="text", text_type=TextType.BOLD, url=None),
                            TextNode(text=" with an ", text_type=TextType.TEXT, url=None),
                            TextNode(text="italic", text_type=TextType.ITALIC, url=None),
                            TextNode(text=" word and a ", text_type=TextType.TEXT, url=None),
                            TextNode(text="code block", text_type=TextType.CODE, url=None),
                            TextNode(text=" and an ", text_type=TextType.TEXT, url=None),
                            TextNode(text="obi wan image", text_type=TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(text=" and a ", text_type=TextType.TEXT, url=None),
                            TextNode(text="link", text_type=TextType.LINK, url="https://boot.dev")                                 
                             ])

if __name__ == "__main__":
    unittest.main()
