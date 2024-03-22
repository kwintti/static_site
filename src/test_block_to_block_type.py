import unittest

from main import block_to_block_type


class Test(unittest.TestCase):
    def test_block_to_block_type(self):
        text = """1.
2.
3.
4.
5.
6.
7.
8."""
        text_result = "ordered_list"
        self.assertEqual(block_to_block_type(text), text_result)

    def test_unordered(self):
        text = """-
-
-
-
-
-
-"""
        text_result = "unordered_list"
        self.assertEqual(block_to_block_type(text), text_result)

    def test_heading(self):
        text = "# Heading hello"
        text_result = "heading"
        self.assertEqual(block_to_block_type(text), text_result)

    def test_code(self):
        text = "``` Some Code here ```"
        text_result = "code"
        self.assertEqual(block_to_block_type(text), text_result)

    def test_code_2(self):
        text = """```
Some Code here
Moro code
the End ```"""
        text_result = "code"
        self.assertEqual(block_to_block_type(text), text_result)

    def test_quote(self):
        text = """> Some comment here
> Moro comment
> end of comment"""
        text_result = "quote"
        self.assertEqual(block_to_block_type(text), text_result)

    def test_paragraph(self):
        text = "This is boring paragraph"
        text_result = "paragraph"
        self.assertEqual(block_to_block_type(text), text_result)


if __name__ == "__main__":
    unittest.main()

