from textnode import TextType, TextNode
from functions.extract_markdown import extract_markdown_images

def split_nodes_image(old_nodes):
  new_nodes = []

  for old_node in old_nodes:
    if old_node.text_type != TextType.PLAIN:
      new_nodes.append(old_node)
    else:
      original_text = old_node.text
      imgs = extract_markdown_images(original_text)
      if len(imgs) == 0:
        new_nodes.append(old_node)
      else:
        for image_alt, image_link in imgs:
          sections = original_text.split(f"![{image_alt}]({image_link})", 1)
          senction_before = sections[0]
          section_after = sections[1]

          if len(senction_before) > 0:
            new_nodes.append(TextNode(senction_before, TextType.PLAIN))

          new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

          original_text = section_after

        # If there are still text we add it as PLAIN
        if len(original_text) != 0:
          new_nodes.append(TextNode(original_text, TextType.PLAIN))
        
        

  return new_nodes