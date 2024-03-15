from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    site = TextNode("kokeilu", "bold", "www.google.com")
    site.url = "www.google.com"
    html = HTMLNode(props={"href": "www.google.com", "target": "_blank"})
    #test = LeafNode("p", "This is a paragraph of text.")
    #test = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    test = LeafNode(None, "Click me now")
    node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode("div", [LeafNode(None, "1 Normal text"), LeafNode("b", "1 This is bold text")]),
                ],
    )

    print(node.to_html())


main()
