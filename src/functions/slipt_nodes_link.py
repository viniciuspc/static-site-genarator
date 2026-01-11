from textnode import TextType, TextNode
from functions.extract_markdown import extract_markdown_links

def split_nodes_link(old_nodes):
  new_nodes = []

  for old_node in old_nodes:
    if old_node.text_type != TextType.PLAIN:
      new_nodes.append(old_node)
    else:
      original_text = old_node.text
      links = extract_markdown_links(original_text)
      if len(links) == 0:
        new_nodes.append(old_node)
      else:
        for link_text, link_target in links:
          sections = original_text.split(f"[{link_text}]({link_target})", 1)
          senction_before = sections[0]
          section_after = sections[1]

          if len(senction_before) > 0:
            new_nodes.append(TextNode(senction_before, TextType.PLAIN))

          new_nodes.append(TextNode(link_text, TextType.LINK, link_target))

          original_text = section_after

        # If there are still text we add it as PLAIN
        if len(original_text) != 0:
          new_nodes.append(TextNode(original_text, TextType.PLAIN))
        
        

  return new_nodes