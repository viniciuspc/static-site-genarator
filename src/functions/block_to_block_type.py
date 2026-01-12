from blocktype import BlockType

def block_to_block_type(block):
  for i in range(1,6):
    if block.startswith(f"{i*'#'} "):
      return BlockType.HEADING
  
  block_lines = block.strip().split("\n")
  if len(block_lines) >= 2 and block_lines[0] == "```" and block_lines[-1] == "```":
    return BlockType.CODE
  
  is_quote_block = True
  for line in block_lines:
    if not line.startswith(">"):
      is_quote_block = False
      break
    
  if is_quote_block:
    return BlockType.QUOTE
  
  is_unordered_list = True
  for line in block_lines:
    if not line.startswith("-"):
      is_unordered_list = False
      break
    
  if is_unordered_list:
    return BlockType.UNORDERED_LIST
  
  is_ordered_list = True
  for i in range(len(block_lines)):
    line = block_lines[i]
    if not line.startswith(f"{i+1}. "):
      is_ordered_list = False
      break
    
  if is_ordered_list:
    return BlockType.ORDERED_LIST
  
  return BlockType.PARAGRAPH
  