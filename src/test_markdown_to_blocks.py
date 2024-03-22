import unittest

from main import markdown_to_blocks


class Test(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        text_result = ["This is **bolded** paragraph",
                       "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", 
                       "* This is a list\n* with items"
                       ]
        self.assertEqual(markdown_to_blocks(text), text_result)

    def test_markdown_to_blocks2(self):
        text = """

This is **bolded** paragraph

* Hello

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items





        """
        text_result = ["This is **bolded** paragraph",
                       "* Hello",
                       "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", 
                       "* This is a list\n* with items"
                       ]
        self.assertEqual(markdown_to_blocks(text), text_result)


if __name__ == "__main__":
    unittest.main()
