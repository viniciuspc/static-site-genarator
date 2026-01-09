import unittest

from textnode import TextNode, TextType
from functions.text_node_to_html_node import text_node_to_html_node
  
class TestFunctions(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")
    
  def test_bold(self):
    node = TextNode("This is a bold text node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a bold text node")
    
  def test_italic(self):
    node = TextNode("This is a italic text node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is a italic text node")
    
  def test_code(self):
    node = TextNode("This is a code text node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is a code text node")
    
  def test_link(self):
    node = TextNode("This is a link text node", TextType.LINK, "https://google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a link text node")
    self.assertEqual(html_node.props, {"href": "https://google.com"})
    
  def test_image(self):
    node = TextNode("This is a image text node", TextType.IMAGE, "https://google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "This is a image text node"})

    
if __name__ == "__main__":
    unittest.main()