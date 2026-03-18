import re

from leafnode import LeafNode
from textnode import TextNode, TextType
from enum import Enum

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    U_LIST="unordered_list"
    O_LIST="ordered_list"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
        else:
            old_node_text = old_node.text
            split_words = old_node_text.split(delimiter)
            count = old_node_text.count(delimiter)
            if count % 2 != 0:
                raise Exception("invalid Markdown syntax")

            for i in range(len(split_words)):
                if i % 2 != 0:
                    res.append(TextNode(split_words[i], text_type))
                else:
                    if split_words[i] != "":
                        res.append(TextNode(split_words[i], TextType.TEXT))
    return res


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
        else:
            text = old_node.text
            extracted = extract_markdown_images(old_node.text)
            for image_alt, image_link in extracted:
                sections = text.split(f"![{image_alt}]({image_link})", 1)
                if sections[0]:
                    res.append(TextNode(sections[0], TextType.TEXT))
                res.append(TextNode(image_alt, TextType.IMAGE, image_link))
                text = sections[1]
            if text:
                res.append(TextNode(text, TextType.TEXT))
    return res


def split_nodes_link(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
        else:
            text = old_node.text
            extracted = extract_markdown_links(old_node.text)
            for link_text, link_url in extracted:
                sections = text.split(f"[{link_text}]({link_url})", 1)
                if sections[0]:
                    res.append(TextNode(sections[0], TextType.TEXT))
                res.append(TextNode(link_text, TextType.LINK, link_url))
                text = sections[1]
            if text:
                res.append(TextNode(text, TextType.TEXT))
    return res


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown):
    block_arr = markdown.split("\n\n")
    block_arr = [item.strip() for item in block_arr if item.strip()]
    return block_arr

def is_unordered_list(block):
    lines = block.split("\n")

    for line in lines:
        if not line.startswith("- "):
            return False

    return True

def is_ordered_list(block):
    lines = block.split("\n")
    count=1

    for line in lines:
        if not line.startswith(f"{count}."):
            return False
        count+=1

    return True

def block_to_block_type (block):
    if re.match(r"^(#{1,6}) (.+)", block):
        return BlockType.HEADING
    elif re.match(r"^```\n([\s\S]*?)```", block):
        return BlockType.CODE
    elif re.match(r"^>(.+)", block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.U_LIST
    elif is_ordered_list(block):
        return BlockType.O_LIST
    else:
        return BlockType.PARAGRAPH