import re
import textwrap

from helpers.utils import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    text_node_to_html_node,
    text_to_textnodes,
)

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode


def text_to_children(text):
    filtered_text= " ".join(text.split())
    block_type = block_to_block_type(text)
    tag, children = None, None
    if block_type == BlockType.HEADING:
        hash_count = 0
        for char in filtered_text:
            if char == "#":
                hash_count += 1
            else:
                break
        tag = f"h{hash_count}"
        children = text_to_textnodes(filtered_text[hash_count+1:])
        html_children = [text_node_to_html_node(child) for child in children]
    elif block_type == BlockType.PARAGRAPH:
        tag = "p"
        children = text_to_textnodes(filtered_text)
        html_children = [text_node_to_html_node(child) for child in children]
    elif block_type == BlockType.QUOTE:
        tag = "blockquote"
        children = text_to_textnodes(filtered_text[2:])
        html_children = [text_node_to_html_node(child) for child in children]
    elif block_type == BlockType.U_LIST or block_type == BlockType.O_LIST:
        tag = "ul" if block_type == BlockType.U_LIST else "ol"
        html_children=[]
        for item in text.split("\n"):
            item_text=re.sub(r'\d+\.\s', '', item) if block_type == BlockType.O_LIST else item[2:]
            sub_children=text_to_textnodes(item_text)
            sub_children_html=[text_node_to_html_node(child) for child in sub_children]
            child_node=ParentNode("li", sub_children_html)
            html_children.append(child_node)
    elif block_type == BlockType.CODE:
        tag="pre"
        code_text = textwrap.dedent(text[3:-3]).lstrip("\n")
        html_children= [ParentNode("code", [LeafNode(None, code_text)])]
    
    return {"tag": tag, "children": html_children}


def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in md_blocks:
        children_dict = text_to_children(block)
        tag, children= children_dict["tag"], children_dict["children"]
        html_nodes.append(ParentNode(tag, children))

    final_node = ParentNode("div", html_nodes)
    return final_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
        
    raise Exception("no title found")