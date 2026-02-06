from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_textnodes
from textnode import TextNode, TextType
import unittest


class TestInline(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        nodes = [TextNode("This is plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_unmatched_delimiter(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

class TestSplitNodes(unittest.TestCase):


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
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
    def test_multiple_images_with_text_between(self):
        node = TextNode(
            "Start ![first](url1) middle ![second](url2) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![first](url1) some text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode(" some text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
        )
    
    def test_multiple_links_with_text_between(self):
        node = TextNode(
            "Start [first](url1) middle [second](url2) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.LINK, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.LINK, "url2"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_link_at_start(self):
        node = TextNode(
            "[first](url1) some text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "url1"),
                TextNode(" some text after", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_no_links_or_images(self):
        node = TextNode(
            "This is plain text without links or images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images(split_nodes_links([node]))
        self.assertListEqual(
            [TextNode("This is plain text without links or images.", TextType.TEXT)],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = "This is a simple text."
        result = text_to_textnodes(text)
        expected = [TextNode("This is a simple text.", TextType.TEXT)]
        self.assertEqual(result, expected)
    
    def test_text_to_textnodes_empty(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_text_to_textnodes_complex(self):
        text = "This is **bold** and _italic_ text with a [link](url) and an ![image](img_url)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img_url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_code(self):
        text = "Here is some `code` in the text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in the text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_text_to_textnodes_multiple_formats_multiple_images_and_url(self):
        text = "Here is an ![image1](img1_url) and another ![image2](img2_url) with a [link1](url1) and [link2](url2)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "img1_url"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "img2_url"),
            TextNode(" with a ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_no_special_formats(self):
        text = "Just a regular sentence without any special formatting."
        result = text_to_textnodes(text)
        expected = [TextNode("Just a regular sentence without any special formatting.", TextType.TEXT)]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()