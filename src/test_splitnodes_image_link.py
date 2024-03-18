import unittest

from main import split_nodes_image, split_nodes_links
from textnode import TextNode


class Test(unittest.TestCase):
    def test_images(self):
        type_txt = "text"
        type_img = "image"
        node = TextNode("tässsä ei ole kuvia", type_txt)
        node1 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) vähän tekstiä ![kolmas image](http://image.co/23434.png) lisää tekstiä ![neljäs img](http://kuva.png) hello.", "text")
        node2 = TextNode("2 This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) vähän tekstiä ![kolmas image](http://image.co/23434.png) lisää tekstiä ![neljäs img](http://kuva.png) hello.", "text")
        self.assertEqual(split_nodes_image([node, node1, node2]), [TextNode("tässsä ei ole kuvia", type_txt), TextNode("This is text with an ", type_txt), TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", type_txt), TextNode("second image", "image", "https://i.imgur.com/3elNhQu.png"), TextNode(" vähän tekstiä ", type_txt), TextNode("kolmas image", type_img, "http://image.co/23434.png"), TextNode(" lisää tekstiä ", type_txt), TextNode("neljäs img", type_img, "http://kuva.png"), TextNode(" hello.", type_txt), TextNode("2 This is text with an ", type_txt), TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", type_txt), TextNode("second image", "image", "https://i.imgur.com/3elNhQu.png"), TextNode(" vähän tekstiä ", type_txt), TextNode("kolmas image", type_img, "http://image.co/23434.png"), TextNode(" lisää tekstiä ", type_txt), TextNode("neljäs img", type_img, "http://kuva.png"), TextNode(" hello.", type_txt)])

    def test_links(self):
        type_txt = "text"
        type_img = "link"
        node = TextNode("tässsä ei ole kuvia", type_txt)
        node1 = TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png) vähän tekstiä [kolmas image](http://image.co/23434.png) lisää tekstiä [neljäs img](http://kuva.png) hello.", "text")
        node2 = TextNode("2 This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png) vähän tekstiä [kolmas image](http://image.co/23434.png) lisää tekstiä [neljäs img](http://kuva.png) hello.", "text")
        self.assertEqual(split_nodes_links([node, node1, node2]), [TextNode("tässsä ei ole kuvia", type_txt), TextNode("This is text with an ", type_txt), TextNode("image", type_img, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", type_txt), TextNode("second image", type_img, "https://i.imgur.com/3elNhQu.png"), TextNode(" vähän tekstiä ", type_txt), TextNode("kolmas image", type_img, "http://image.co/23434.png"), TextNode(" lisää tekstiä ", type_txt), TextNode("neljäs img", type_img, "http://kuva.png"), TextNode(" hello.", type_txt), TextNode("2 This is text with an ", type_txt), TextNode("image", type_img, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", type_txt), TextNode("second image", type_img, "https://i.imgur.com/3elNhQu.png"), TextNode(" vähän tekstiä ", type_txt), TextNode("kolmas image", type_img, "http://image.co/23434.png"), TextNode(" lisää tekstiä ", type_txt), TextNode("neljäs img", type_img, "http://kuva.png"), TextNode(" hello.", type_txt)])



if __name__ == "__main__":
    unittest.main()

