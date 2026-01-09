import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
  
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
    
class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode(tag="p", value="Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
  def test_leaf_to_html_b(self):
    node = LeafNode(tag="b", value="Hello, world!")
    self.assertEqual(node.to_html(), "<b>Hello, world!</b>")
    
  def test_leaf_to_html_link(self):
    props = {
      "href": "https://www.google.com",
      "target": "_blank",
    }
    node = LeafNode(tag="a", value="Google", props=props)
    self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Google</a>')
    
class TestParentNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode(tag="span", value="child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
  def test_to_html_with_link_children(self):
    props = {
      "href": "https://www.google.com",
      "target": "_blank",
    }
    child_node = LeafNode(tag="a", value="Google", props=props)
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com" target="_blank">Google</a></div>')

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode(tag="b", value="grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )
    
  def test_to_html_with_grandchildren_with_props(self):
    grandchild_node = LeafNode(tag="b", value="grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode(tag="div", children=[child_node], props={"class":"card"})
    self.assertEqual(
        parent_node.to_html(),
        '<div class="card"><span><b>grandchild</b></span></div>',
    )
    
if __name__ == "__main__":
    unittest.main()