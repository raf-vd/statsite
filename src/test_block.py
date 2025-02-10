import unittest
from block import *

class TestFunction(unittest.TestCase):
    def test_block_to_block_type(self):
        # 1 #
        txt = """# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it."""
        self.assertEqual(block_to_block_type(txt), BlockType.HEADING)

        # 2 #
        txt ="""``` code block 
some shitty code
end of block```"""
        self.assertEqual(block_to_block_type(txt), BlockType.CODE)

        # 3 #
        txt = """> quoted
> text block    
>"""    
        # 4 #
        self.assertEqual(block_to_block_type(txt), BlockType.QUOTE)

        txt = """* an example
- of an unsorted list
* even the - isn't a problem
* """
        # 5 #
        self.assertEqual(block_to_block_type(txt), BlockType.UNORDERED_LIST)

        txt = """1. First line
2. Second line
3. Third line
4. Fourth line"""    
        self.assertEqual(block_to_block_type(txt), BlockType.ORDERED_LIST)

        # 6 #
        txt = "just some random text, so this should be a paragraph"
        self.assertEqual(block_to_block_type(txt),  BlockType.PARAGRAPH)

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

if __name__ == "__main__":
    unittest.main()
