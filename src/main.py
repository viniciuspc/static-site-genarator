from textnode import TextNode, TextType
def main():
  print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))
  print(TextNode("This is some plain text", TextType.PLAIN))
  print(TextNode("This is some bold text", TextType.BOLD))
  
if __name__ == "__main__":
  main()