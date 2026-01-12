def markdown_to_blocks(markdown):
  blocks = []
  for block in markdown.split("\n\n"):
    if len(block) > 0:
      blocks.append(block.strip())
      
  return blocks