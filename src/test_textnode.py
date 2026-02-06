import unittest

from textnode import TextNode, TextType



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 =  TextNode("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node,node2)

    def test_URL(self):
        node = TextNode("text", TextType.LINK)
        node2 = TextNode("text", TextType.LINK, "www.youtube.com")
        self.assertNotEqual(node,node2)
    
    def test_difftext(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node,node2)

    def test_checkeq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("wrongtext",TextType.LINK,"www.youtube.com")
        self.assertNotEqual(node,node2)



if __name__ == "__main__":
    unittest.main()