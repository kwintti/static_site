from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
import re
import os
import shutil


def main():
    copy_files_from_directory("static/", "public/")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content/", "template.html", "public/")

def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


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
            if val.url is not None:
                output.append(TextNode(val.text, val.text_type, val.url))
            else:
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
            if len(splitted) != 0:
                output.append(TextNode(splitted[0], val.text_type))
                right_side = splitted[-1]
            output.append(TextNode(image_tup[0], "image", image_tup[1]))
            if len(splitted) == 2 and len(links) == 1:
                output.append(TextNode(right_side, val.text_type))
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
            if val.url is not None:
                output.append(TextNode(val.text, val.text_type, val.url))
            else:
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
                if len(splitted) != 0:
                    output.append(TextNode(splitted[0], val.text_type))
                output.append(TextNode(image_tup[0], "link", image_tup[1]))
                if len(splitted) > 1 and num_iterations == 0:
                    output.append(TextNode(splitted[1], val.text_type))
                right_side = splitted[-1]
                continue
            splitted = val.text.split(f"[{image_tup[0]}]({image_tup[1]})", 1)
            splitted = [i for i in splitted if i != ""]
            if len(splitted) != 0:
                output.append(TextNode(splitted[0], val.text_type))
                right_side = splitted[-1]
            output.append(TextNode(image_tup[0], "link", image_tup[1]))
            if len(splitted) == 2 and len(links) == 1:
                output.append(TextNode(right_side, val.text_type))
        new_nodes.extend(output)
        right_side = []
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, "text")
    bolds = split_nodes_delimiter([node], "**", "bold")
    italic = split_nodes_delimiter(bolds, "*", "italic")
    code = split_nodes_delimiter(italic, "`", "code")
    image = split_nodes_image(code)
    link = split_nodes_links(image)

    return link


def markdown_to_blocks(markdown):
    splitted = markdown.split("\n\n")
    splitted = [i.strip() for i in splitted]
    splitted = [i for i in splitted if i != ""]

    return splitted


def block_to_block_type(block):
    headings = bool(re.match(r"^#{1,6}\s", block))
    if headings:
        return "heading"

    code = bool(re.match(r"```([\s\S]*?)```", block))
    if code:
        return "code"

    quotes_true_list = []
    for line in block.splitlines():
        if line[0] != ">":
            quotes_true_list.append(False)
        else:
            quotes_true_list.append(True)
    if all(quotes_true_list):
        return "quote"

    un_list_true_list = []
    for line in block.splitlines():
        if line[0] == "*" or line[0] == "-":
            un_list_true_list.append(True)
        else:
            un_list_true_list.append(False)
    if all(un_list_true_list):
        return "unordered_list"

    ord_list_true_list = []
    incr = 1
    for line in block.splitlines():
        if line.split(" ", 1)[0] == f"{incr}.":
            ord_list_true_list.append(True)
        else:
            ord_list_true_list.append(False)
        incr += 1

    if all(ord_list_true_list):
        return "ordered_list"

    return "paragraph"


def quote_to_htmlnode(quote):
    striped_quote = ""
    for line in quote.splitlines():
        striped_quote += line.split(">", 1)[-1].strip() + " "
    striped_quote = striped_quote.strip()
    node = LeafNode("blockquote", striped_quote)
    return node


def u_list_to_htmlnode(u_list):
    list_items = []
    for line in u_list.splitlines():
        if line[0] == "*":
            value = line.split("*", 1)[-1].strip()
            txt_nodes = text_to_textnodes(value)
            all_nodes = []
            for node in txt_nodes:
                to_html_node = text_node_to_html_node(node)
                all_nodes.append(to_html_node)
            list_items.append(ParentNode("li", all_nodes))
        if line[0] == "-":
            value = line.split("-", 1)[-1].strip()
            txt_nodes = text_to_textnodes(value)
            all_nodes = []
            for node in txt_nodes:
                to_html_node = text_node_to_html_node(node)
                all_nodes.append(to_html_node)
            list_items.append(ParentNode("li", all_nodes))
    node = ParentNode("ul", list_items)
    return node


def ord_list_to_htmlnode(ord_list):
    list_items = []
    for line in ord_list.splitlines():
        value = line.split(".", 1)[-1].strip()
        txt_nodes = text_to_textnodes(value)
        all_nodes = []
        for node in txt_nodes:
            to_html_node = text_node_to_html_node(node)
            all_nodes.append(to_html_node)
        list_items.append(ParentNode("li", all_nodes))
    node = ParentNode("ol", list_items)
    return node


def code_to_htmlnode(code):
    lines = []
    code_items = ""
    for line in code.splitlines():
        if line[:3] == "```" and line[-3:] == "```":
            splited = line.split("```", 2)
            splited = [i for i in splited if i != ""] 
            lines.extend(splited)
            continue
        if line[:3] == "```":
            lines.append(line.split("```", 1)[-1].strip())
        if line[-3:] == "```":
            lines.append(line.split("```", 1)[0].strip())
    for lin in lines:
        code_items += lin + " "
    leaf = LeafNode("code", code_items)
    node = ParentNode("pre", [leaf])
    return node


def heading_to_htmlnode(heading):
    count = 0
    for hed in heading[:6]:
        if hed == "#":
            count += 1
    value = heading[count:].strip()
    level = f"h{count}"
    txt_nodes = text_to_textnodes(value)
    all_nodes = []
    for node in txt_nodes:
        to_html_node = text_node_to_html_node(node)
        all_nodes.append(to_html_node)
    node = ParentNode(level, all_nodes)

    return node


def paragraph_to_htmlnode(paragraph):
    return LeafNode("p", paragraph)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    build_blocks_up = []
    for block in blocks:
        blc_type = block_to_block_type(block)
        if blc_type == "quote":
            build_blocks_up.append(quote_to_htmlnode(block))
        if blc_type == "ordered_list":
            build_blocks_up.append(ord_list_to_htmlnode(block))
        if blc_type == "unordered_list":
            build_blocks_up.append(u_list_to_htmlnode(block))
        if blc_type == "code":
            build_blocks_up.append(code_to_htmlnode(block))
        if blc_type == "heading":
            build_blocks_up.append(heading_to_htmlnode(block))
        if blc_type == "paragraph":
            txtNodes = text_to_textnodes(block)
            allNodes = []
            for nd in txtNodes:
                toHtml = text_node_to_html_node(nd)
                allNodes.append(toHtml)
            toParentNode = ParentNode("p", allNodes)
            build_blocks_up.append(toParentNode)

    finalHtml = ParentNode("div", build_blocks_up)
    return finalHtml


def copy_files_from_directory(from_path, to_path):
    if os.path.exists(from_path) is False:
        raise Exception("Path doesn't exist")
    if os.path.exists(to_path) is False:
        os.mkdir(to_path)
    list_files = os.listdir(from_path)
    for file in list_files:
        is_file = os.path.isfile(os.path.join(from_path, file))
        is_dir = os.path.isdir(os.path.join(from_path, file))
        if is_file:
            shutil.copy(os.path.join(from_path, file), os.path.join(to_path, file))
        if is_dir:
            copy_files_from_directory(os.path.join(from_path, file), os.path.join(to_path, file))


def extract_title(header_md):
    blocks = markdown_to_blocks(header_md)
    for block in blocks:
        type_blc = block_to_block_type(block)
        if type_blc == "heading":
            count = 0
            for letter in block[:6]:
                if letter == "#":
                    count += 1
            if count == 1:
                return block[1:].strip()
    raise Exception("h1 not found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md_file = f.read()
    with open(template_path) as f:
        template_file = f.read()

    title = extract_title(md_file)
    content = markdown_to_html_node(md_file).to_html()
    output_html = template_file.replace("{{ Title }}", title)
    output_html = output_html.replace("{{ Content }}", content)

    dir_path = ""
    dir_path_list = dest_path.split("/")
    for folder in dir_path_list[:-1]:
        dir_path = os.path.join(dir_path, folder)

    if os.path.isdir(dir_path) is False:
        os.makedirs(dir_path)

    with open(dest_path, "w") as f:
        f.write(output_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.exists(dir_path_content) is False:
        raise Exception("Path doesn't exist")
    if os.path.exists(dest_dir_path) is False:
        os.mkdir(dest_dir_path)
    list_files = os.listdir(dir_path_content)
    for file in list_files:
        is_file = os.path.isfile(os.path.join(dir_path_content, file))
        is_dir = os.path.isdir(os.path.join(dir_path_content, file))
        if is_file:
            file_html_name = file.replace(".md", ".html")
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file_html_name))
        if is_dir:
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))


main()
