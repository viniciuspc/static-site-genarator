from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []

  for old_node in old_nodes:
    if old_node.text_type != TextType.PLAIN:
      new_nodes.append(old_node)
    else:
      new_texts = old_node.text.split(delimiter)

      if len(new_texts) % 2 == 0:
        raise Exception("No matching closing delimiter found")
      
      for i in range(len(new_texts)):
        if i % 2 == 0:
          if len(new_texts[i]) > 0:
            new_nodes.append(TextNode(new_texts[i], TextType.PLAIN))
        else:
          new_nodes.append(TextNode(new_texts[i], text_type))

  return new_nodes