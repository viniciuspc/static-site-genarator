import unittest

from textnode import TextNode, TextType
from functions.text_node_to_html_node import text_node_to_html_node
from functions.split_nodes_delimiter import split_nodes_delimiter
  
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

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_code(self):
    node = TextNode("This is text with a `code block` word", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
    ]

    self.assertEqual(new_nodes, expected)

  def test_two_code(self):
    node = TextNode("This is text with a `code block` word and `other code block` word", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word and ", TextType.PLAIN),
        TextNode("other code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN)
    ]

    self.assertEqual(new_nodes, expected)

  def test_code_end(self):
    node = TextNode("This is text with a `code block`", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
    ]

    self.assertEqual(new_nodes, expected)

  def test_code_begin(self):
    node = TextNode("`code block` is a code", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("code block", TextType.CODE),
        TextNode(" is a code", TextType.PLAIN),
        
    ]

    self.assertEqual(new_nodes, expected)

  def test_only_code(self):
    node = TextNode("`code block`", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("code block", TextType.CODE),
    ]

    self.assertEqual(new_nodes, expected)

  def test_bold(self):
    node = TextNode("Let us see the **code**", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    expected = [
        TextNode("Let us see the ", TextType.PLAIN),
        TextNode("code", TextType.BOLD),
    ]

    self.assertEqual(new_nodes, expected)

  def test_italic(self):
    node = TextNode("_Italy_", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    expected = [
        TextNode("Italy", TextType.ITALIC),
    ]

    self.assertEqual(new_nodes, expected)

  def test_multiple_old_nodes(self):
    nodes = [
        TextNode("Let us see the **code**", TextType.PLAIN),
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word and ", TextType.PLAIN),
        TextNode("_Italy_", TextType.PLAIN),
        TextNode("other code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
        TextNode(" OMG an other `code`", TextType.PLAIN)
    ]
    new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    expected = [
        TextNode("Let us see the ", TextType.PLAIN),
        TextNode("code", TextType.BOLD),
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word and ", TextType.PLAIN),
        TextNode("Italy", TextType.ITALIC),
        TextNode("other code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
        TextNode(" OMG an other ", TextType.PLAIN),
        TextNode("code", TextType.CODE),
    ]

    self.assertEqual(new_nodes, expected)

    
if __name__ == "__main__":
    unittest.main()