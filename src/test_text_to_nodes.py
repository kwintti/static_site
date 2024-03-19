import unittest

from main import text_to_textnodes
from textnode import TextNode


class Test(unittest.TestCase):
    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev) [toka linkki](www.google.com) ![toka kuva](imgur.com/kuva.png) hello"
        text_to_textnodes(text)
        self.assertEqual(text_to_textnodes(text), [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
            TextNode(" ", "text"),
            TextNode("toka linkki", "link", "www.google.com"),
            TextNode(" ", "text"),
            TextNode("toka kuva", "image", "imgur.com/kuva.png"),
            TextNode(" hello", "text"),
            ])




if __name__ == "__main__":
    unittest.main()

