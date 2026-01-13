from functions.copy_tree import copy_tree
from functions.generate_page import generate_page
def main():
  copy_tree("static/","public/")
  
  generate_page("content/index.md", "template.html", "public/index.html")
  
  
if __name__ == "__main__":
  main()