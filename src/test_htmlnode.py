import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode,text_node_to_html_node
from textnode import TextNode,TextType


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        props = {"href": "https://www.google.com","target": "_blank",}
        node = HTMLNode(None,None,None,props)
        node2 = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(),node2)

    def test_propsnone(self):
        props = {}
        node = HTMLNode(None,None,None,props)
        node2 = ""
        self.assertEqual(node.props_to_html(),node2)

    def test_propsnostring(self):
        props = {"data-id": 123}
        node = HTMLNode(None,None,None,props)
        node2 = " data-id=\"123\""
        self.assertEqual(node.props_to_html(),node2)

    def test_repr_includes_tag_and_value(self):
        node = HTMLNode("p", "hello", [], {"class": "greeting"})
        text = node.__repr__()

        self.assertIn("p", text)
        self.assertIn("hello", text)
        self.assertIn("class", text)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_href(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',)

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("span", "Hi", {"class": "greeting", "id": "g1"})
        html = node.to_html()
        # Order depends on dict insertion, so just check substrings:
        self.assertTrue(html.startswith("<span"))
        self.assertIn('class="greeting"', html)
        self.assertIn('id="g1"', html)
        self.assertTrue(html.endswith(">Hi</span>"))

    def test_leaf_to_html_no_tag_returns_value(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_when_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        rep = repr(node)
        self.assertIn("LeafNode", rep)
        self.assertIn("p", rep)
        self.assertIn("Hello", rep)
        self.assertIn("greeting", rep)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)
    
    def test_single_child_text(self):
        child = LeafNode(None, "hello")
        parent = ParentNode("p", [child])
        self.assertEqual(parent.to_html(), "<p>hello</p>")

    def test_multiple_children_mixed_tags(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
        ]
        parent = ParentNode("p", children)
        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> and <i>italic</i></p>",
        )

    def test_parent_with_attributes(self):
        child = LeafNode(None, "content")
        parent = ParentNode("div", [child], props={"class": "box", "id": "main"})
        # Order of props may vary depending on your implementation
        html = parent.to_html()
        self.assertIn("<div", html)
        self.assertIn('class="box"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.endswith("content</div>"))

    def test_nested_parents(self):
        inner = ParentNode("span", [LeafNode(None, "inner")])
        outer = ParentNode("div", [inner])
        self.assertEqual(
            outer.to_html(),
            "<div><span>inner</span></div>",
        )

    def test_no_tag_raises(self):
        child = LeafNode(None, "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_no_children_raises(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

class TestNodetoHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertIsNone(html_node.props)

    def test_italic(self):
        node = TextNode("slanted", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "slanted")
        self.assertIsNone(html_node.props)

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")
        self.assertIsNone(html_node.props)

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("A bear", TextType.IMAGE, "https://example.com/bear.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/bear.png", "alt": "A bear"},
        )
    
    def test_bad_type_raises(self):
        node = TextNode("???", "not-a-real-type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()