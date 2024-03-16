from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    site = TextNode("Kiva kuva", "image", "imgur.fi/logo.png")
    site.text
    site.text_type
    site.url = "www.google.com"
    html = HTMLNode(props={"href": "www.google.com", "target": "_blank"})
    #test = LeafNode("p", "This is a paragraph of text.")
    #test = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    #test = LeafNode(None, "Click me now")
    #node = ParentNode(
    #        "p",
    #        [
    #            LeafNode("b", "Bold text"),
    #            LeafNode(None, "Normal text"),
    #            LeafNode("i", "italic text"),
    #            LeafNode(None, "Normal text"),
    #            ParentNode("div", [LeafNode(None, "1 Normal text"), LeafNode("b", "1 This is bold text")]),
    #            ],
    #)

    #print(node.to_html())
    #print(text_node_to_html_node(site))
    #node = TextNode("This is text with a `code block` word and it continues `hello world`", "text")
    #node2 = TextNode("2 This is text with a `code block` word and it continues `hello world`", "text")
    #new_nodes = split_nodes_delimiter([node, node2, "This is raw text, no node"], "`", "code")



def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text).to_html()
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text).to_html()
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text).to_html()
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text).to_html()
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url}).to_html()
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}).to_html()


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for val in old_nodes:
        output = []
        if isinstance(val, TextNode) is False:
            output.append(val)
            new_nodes.extend(output)
            continue
        if val.text.count(delimiter) % 2 != 0:
            raise Exception("Missing closing tag")
        splitted = val.text.split(delimiter)
        splitted = [i for i in splitted if i != ""]
        orig_text = val.text_type
        for i, split in enumerate(splitted):
            if i % 2 == 0:
                output.append(TextNode(split, orig_text))
                continue
            output.append(TextNode(split, text_type))
        new_nodes.extend(output)
    return new_nodes

main()
