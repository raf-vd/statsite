import re
import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, HTMLTag
from leafnode import LeafNode
from parentnode import ParentNode

class TestFunction(unittest.TestCase):
    def test_block_to_block_type(self):
        # 1 #
        txt = """# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        self.assertEqual(block_to_block_type(txt), "heading")

        # 2 #
        txt ="""``` \w code block 
some shitty code
end of block```"""
        self.assertEqual(block_to_block_type(txt), "code")

        # 3 #
        txt = """> quoted
> text block    
>"""    
        # 4 #
        self.assertEqual(block_to_block_type(txt), "quote")

        txt = """* an example
- of an unsorted list
* even the - isn't a problem
* """
        # 5 #
        self.assertEqual(block_to_block_type(txt), "unordered_list")

        txt = """1. First line
2. Second line
3. Third line
4. Fourth line"""    
        self.assertEqual(block_to_block_type(txt), "ordered_list")

        # 6 #
        txt = "just some random text, so this should be a paragraph"
        self.assertEqual(block_to_block_type(txt), "paragraph")

#----------------------------------------------------------------------------------------#
    def test_markdown_to_blocks(self):
        # 1 #
        txt = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertListEqual(markdown_to_blocks(txt),['# This is a heading', 
                                                     'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                                                     '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                                                    ])

        # 2 #
        txt = """
        # This is a heading

        
This is a paragraph of text. It has some **bold** and *italic* words inside of it.




* This is the first list item in a list block
* This is a list item
* This is another list item


"""
        self.assertListEqual(markdown_to_blocks(txt),['# This is a heading', 
                                                     'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                                                     '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                                                    ])

#----------------------------------------------------------------------------------------#

def markdown_to_blocks(markdown):
    md_blocks = []
    if markdown:
        blocks = markdown.split("\n\n")
        for block in blocks:
            stripped = block.strip().strip("\n")
            if stripped:
                md_blocks.append(stripped)
    return md_blocks


def block_to_block_type(block_of_markdown):
    
    pattern = r"^#{1,6}"
    if re.findall(pattern, block_of_markdown):return "heading"

    pattern = r"^```[\s\S]*```$"
    if re.findall(pattern, block_of_markdown):return "code"

    pattern = r"^(>.*\n)*>.*$"
    if re.findall(pattern, block_of_markdown):return "quote"

    pattern = r"^([\*-] .*\n)*[\*-] .*$"
    if re.findall(pattern, block_of_markdown):return "unordered_list"

    # Last check, if this fails => default or paragraph
    pattern = r"^(1\. .*\n|(\d+)\.\s.*\n)*\d\.\s.*$"    # Check for 'N. ' at the start of each line; including the last if empty"
    if re.findall(pattern, block_of_markdown, re.MULTILINE):
        lines = block_of_markdown.splitlines()          # Check for sequential numbers starting at 1
        if lines:
            for i, line in enumerate(lines, start=1):
                if not re.match(rf"^{i}\. .+", line):  # Check if each line matches the number
                    return "paragraph" 
            return "ordered_list"
    
    return "paragraph"  # Failed all type checks => default to paragraph


def main():
    pass


main()

if __name__ == "__main__":
    unittest.main()