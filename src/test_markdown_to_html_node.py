import unittest

from main import markdown_to_html_node


class Test(unittest.TestCase):
    def test_markdown_to_html_node(self):
        self.maxDiff = None
        text = """# This is heading

This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line and a link follows [linking](www.google.com)

* This is a list
* with items"""
        text_result = """<div><h1>This is heading</h1><p>This is <b>bolded</b> paragraph</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here
This is the same paragraph on a new line and a link follows <a href="www.google.com">linking</a></p><ul><li>This is a list</li><li>with items</li></ul></div>"""


        self.assertEqual(markdown_to_html_node(text).to_html(), text_result)


if __name__ == "__main__":
    unittest.main()
