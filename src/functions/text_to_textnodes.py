from functions.split_nodes_delimiter import split_nodes_delimiter
from functions.slipt_nodes_image import split_nodes_image
from functions.slipt_nodes_link import split_nodes_link
from textnode import TextNode, TextType

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.PLAIN)]
  new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
  new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
  new_nodes = split_nodes_image(new_nodes)
  new_nodes = split_nodes_link(new_nodes)

  return new_nodes
