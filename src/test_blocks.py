from textwrap import dedent
import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdowntoBlock(unittest.TestCase):
    

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

        def test_markdown_to_blocks_empty(self):
            md = ""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [])

        def test_block_to_block_type(self):
            self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
            self.assertEqual(
                block_to_block_type("```\ncode block\n```"), BlockType.CODE
            )
            self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
            self.assertEqual(
                block_to_block_type("- List item 1\n- List item 2"),
                BlockType.UNORDERED_LIST,
            )
            self.assertEqual(
                block_to_block_type("1. First item\n2. Second item"),
                BlockType.ORDERED_LIST,
            )
            self.assertEqual(
                block_to_block_type("This is a simple paragraph."),
                BlockType.PARAGRAPH,
            )
        
        def test_block_to_block_type_mixed_ordered_list(self):
            md = "1. First item\n2. Second item\n1. Third item"
            self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

        def test_block_to_block_type_ordered_list_single_item(self):
            md = "1. Only item"
            self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

class TestMarkdownToHtmlNodes(unittest.TestCase):
    from blocks import markdown_to_html_node
    from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_multiple_paragraphs_with_inline(self):
        md = """
This paragraph has **bold** and *italic* and `code`.

Another paragraph with a [link](https://example.com) here.

Final paragraph with ![image](https://example.com/img.png) alt text.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Check that you have 3 separate <p> tags
        self.assertIn("<p>This paragraph has <b>bold</b>", html)
        self.assertIn("<p>Another paragraph with a <a", html)
        self.assertIn("<p>Final paragraph with <img", html)

    def test_heading_with_inline_markdown(self):
        md = "## This is a **bold** heading with `code`"
        node = markdown_to_html_node(md) 
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a <b>bold</b> heading with <code>code</code></h2></div>"
        )

    def test_nested_lists(self):
        md = """
- Item 1 with **bold**
- Item 2 with *italic*
- Item 3 with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li>Item 1 with <b>bold</b></li>", html)
        self.assertIn("<li>Item 2 with <i>italic</i></li>", html)

    def test_ordered_list_with_inline(self):
        md = """
1. First **bold** item
2. Second *italic* item
3. Third `code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ol>", html)
        self.assertIn("<li>First <b>bold</b> item</li>", html)

    def test_multiline_quote(self):
        md = """
> This is a quote
> with **bold** text
> across multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<blockquote>", html)
        self.assertIn("<b>bold</b>", html)
                            

if __name__ == "__main__":
    unittest.main()