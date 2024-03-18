from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
import re


def main():
    pass


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


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    right_side = []
    new_nodes = []
    for val in old_nodes:
        links = extract_markdown_images(val.text)
        output = []
        if len(links) == 0:
            output.append(TextNode(val.text, val.text_type))
            new_nodes.extend(output)
            continue
        num_iterations = len(links)
        for link in links:
            num_iterations -= 1
            image_tup = link
            if right_side:
                splitted = right_side.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                splitted = [i for i in splitted if i != ""]
                output.append(TextNode(splitted[0], val.text_type))
                output.append(TextNode(image_tup[0], "image", image_tup[1]))
                if len(splitted) > 1 and num_iterations == 0:
                    output.append(TextNode(splitted[1], val.text_type))
                right_side = splitted[-1]
                continue
            splitted = val.text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            splitted = [i for i in splitted if i != ""]
            output.append(TextNode(splitted[0], val.text_type))
            output.append(TextNode(image_tup[0], "image", image_tup[1]))
            right_side = splitted[-1]

        new_nodes.extend(output)
        right_side = []
    return new_nodes


def split_nodes_links(old_nodes):
    right_side = []
    new_nodes = []
    for val in old_nodes:
        links = extract_markdown_links(val.text)
        output = []
        if len(links) == 0:
            output.append(TextNode(val.text, val.text_type))
            new_nodes.extend(output)
            continue
        num_iterations = len(links)
        for link in links:
            num_iterations -= 1
            image_tup = link
            if right_side:
                splitted = right_side.split(f"[{image_tup[0]}]({image_tup[1]})", 1)
                splitted = [i for i in splitted if i != ""]
                output.append(TextNode(splitted[0], val.text_type))
                output.append(TextNode(image_tup[0], "link", image_tup[1]))
                if len(splitted) > 1 and num_iterations == 0:
                    output.append(TextNode(splitted[1], val.text_type))
                right_side = splitted[-1]
                continue
            splitted = val.text.split(f"[{image_tup[0]}]({image_tup[1]})", 1)
            splitted = [i for i in splitted if i != ""]
            output.append(TextNode(splitted[0], val.text_type))
            output.append(TextNode(image_tup[0], "link", image_tup[1]))
            right_side = splitted[-1]

        new_nodes.extend(output)
        right_side = []
    return new_nodes


main()
