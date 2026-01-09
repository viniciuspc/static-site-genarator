from textnode import TextNode, TexType
def main():
  print(TextNode("This is some anchor text", TexType.LINK, "https://www.boot.dev"))
  print(TextNode("This is some plain text", TexType.PLAIN_TEXT, ""))
  print(TextNode("This is some bold text", TexType.BOLD_TEXT, ""))
  
if __name__ == "__main__":
  main()