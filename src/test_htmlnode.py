import unittest

from htmlnode import HTMLNode
  
class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    props = {
      "href": "https://www.google.com",
      "target": "_blank",
    }

    node = HTMLNode(tag="a",props=props)
    
    expected = ' href="https://www.google.com" target="_blank"'
    
    self.assertEqual(node.props_to_html(), expected)
    
  def test_none_props_to_html(self):

    node = HTMLNode(tag="b", value="bold text")
    self.assertEqual(node.props_to_html(), "")
    
  def test_empty_props_to_html(self):

    node = HTMLNode(tag="b", value="bold text", props={})
    self.assertEqual(node.props_to_html(), "")
    
  def test_to_html_not_implemented(self):
    node = HTMLNode(tag="b", value="bold text")
    self.assertRaises(NotImplementedError, node.to_html)
    
  def test_repr(self):
    node = HTMLNode(tag="b", value="bold text")
    expected = "HTMLNode(Tag: |b|, Value: |bold text|, Children: |None|, Props: ||)"
    self.assertEqual(str(node), expected)
    
    props = {
      "href": "https://www.google.com",
      "target": "_blank",
    }
    
    node = HTMLNode(tag="a", value="Google", props=props)
    expected = "HTMLNode(Tag: |a|, Value: |Google|, Children: |None|, Props: | href=\"https://www.google.com\" target=\"_blank\"|)"
    self.assertEqual(str(node), expected)