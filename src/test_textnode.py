import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        
        
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
        
    def test_not_eq_text(self):
        node = TextNode("This is a text node 1", TextType.PLAIN)
        node2 = TextNode("This is a text node 2", TextType.PLAIN)
        self.assertNotEqual(node, node2)
        
    def test_eq_with_url(self):
        node = TextNode("This is a link node with url", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link node with url", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)
        
    def test_not_eq_with_url(self):
        node = TextNode("This is a link node with url", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link node with url", TextType.LINK, "https://www.example.com")
        self.assertNotEqual(node, node2)
        
    def test_eq_img_with_url(self):
        node = TextNode("This is a link node with url", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link node with url", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)
        
    def test_not_eq_img_with_url(self):
        node = TextNode("This is a image node with url", TextType.IMAGE, "https://www.boot.dev")
        node2 = TextNode("This is a image node with url", TextType.IMAGE, "https://www.example.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()