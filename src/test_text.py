import unittest

from helpers.markdown_to_html import markdown_to_html_node
from textnode import TextNode, TextType
from helpers.utils import (
    BlockType,
    block_to_block_type,
    extract_markdown_images,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestParentNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_single_delimiter_split(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)

        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("a `code` b `more` c", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 5)
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[3].text_type, TextType.CODE)

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)

    def test_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_non_text_nodes_unchanged(self):
        node = TextNode("code", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], node)

    def test_invalid_odd_delimiters(self):
        node = TextNode("This is `broken text", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertListEqual([node], new_nodes)

    def test_split_links_start(self):
        node = TextNode(
            "[hello](https://test.com) world",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("hello", TextType.LINK, "https://test.com"),
                TextNode(" world", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_duplicate(self):
        node = TextNode(
            "[a](url) and [a](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("a", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_text_to_nodes_full_case(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block_type(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE,
        )

        self.assertEqual(
            block_to_block_type("> this is a quote"),
            BlockType.QUOTE,
        )

        self.assertEqual(
            block_to_block_type("- item 1\n- item 2"),
            BlockType.U_LIST,
        )

        self.assertEqual(
            block_to_block_type("1. item 1\n2. item 2"),
            BlockType.O_LIST,
        )

        self.assertEqual(
            block_to_block_type("just a normal paragraph"),
            BlockType.PARAGRAPH,
        )

    def test_paragraphs(self):
            md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

    def test_codeblock(self):
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )


if __name__ == "__main__":
    unittest.main()
