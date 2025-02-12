import unittest
import re
from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_minimal_case(self):
        md = """# This is a simple title"""
        self.assertEqual(extract_title(md),
                         "This is a simple title")

    def test_basic_case(self):
        md = """# This is a simple title
some test
to try out multiple lines"""
        self.assertEqual(extract_title(md),
                         "This is a simple title")

    def test_not_on_first_line_case(self):
        md = """pre title

# This is a simple title
some test
to try out multiple lines"""
        self.assertEqual(extract_title(md),
                         "This is a simple title")

    def test_more_hash_tags(self):
        md = """#### This is a simple title
some test
# Real title
to try out multiple lines"""
        self.assertEqual(extract_title(md),
                         "Real title")

    def test_morethan_1(self):
        md = """# This is a first simple title
some test
# Here is the second one
to try out multiple lines"""
        self.assertEqual(extract_title(md),
                         "This is a first simple title")

    def test_no_title(self):
        md = """+# This is a simple title
some test
to try out multiple lines"""
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
