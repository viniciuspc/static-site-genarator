from htmlnode import ParentNode,LeafNode
from blocktype import BlockType

from functions.markdown_to_blocks import markdown_to_blocks
from functions.block_to_block_type import block_to_block_type
from functions.text_to_textnodes import text_to_textnodes
from functions.text_node_to_html_node import text_node_to_html_node

def markdown_to_html_node(markdown):
  children = []
  blocks = markdown_to_blocks(markdown)
  for block in blocks:
    block_type = block_to_block_type(block)
    match block_type:
      case BlockType.PARAGRAPH:
        paragraph_children = text_to_children(block.replace("\n", " "))
        paragraph_node = ParentNode("p", paragraph_children)
        children.append(paragraph_node)
      case BlockType.HEADING:
        levels = block.split("#")
        text = levels[-1].strip()
        heading_children = text_to_children(text)
        heading_node = ParentNode(f"h{len(levels) - 1}", heading_children)
        children.append(heading_node)
      case BlockType.CODE:
        code_children = LeafNode(block.replace("```\n","").replace("```",""))
        code_node = ParentNode("code", [code_children])
        pre_node = ParentNode("pre", [code_node])
        children.append(pre_node)
      case BlockType.QUOTE:
        quote_children = multiline_block_to_children(block, "> ", "p")
        quote_node = ParentNode("blockquote", quote_children)
        children.append(quote_node)
      case BlockType.UNORDERED_LIST:
        ul_children = multiline_block_to_children(block, "- ", "li")
        ul_node = ParentNode("ul", ul_children)
        children.append(ul_node)
      case BlockType.ORDERED_LIST:
        ol_children = multiline_block_to_children(block, ". ", "li")
        ol_node = ParentNode("ol", ol_children)
        children.append(ol_node)
          
        
  return ParentNode("div", children)
        
def text_to_children(text):
  children = []
  text_nodes = text_to_textnodes(text)
  
  for text_node in text_nodes:
    children.append(text_node_to_html_node(text_node))
    
  return children
    
    
def multiline_block_to_children(block, sep, tag):
  children = []
  itens = block.split("\n")
  for item in itens:
    if len(item) == 0:
      continue
    text = item.split(sep, 1)[-1]
    tag_children = text_to_children(text)
    tag_node = ParentNode(tag, tag_children)
    children.append(tag_node)
    
  return children