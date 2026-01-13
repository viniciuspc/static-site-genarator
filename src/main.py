from functions.copy_tree import copy_tree
from functions.generate_pages_recursive import generate_pages_recursive
def main():
  copy_tree("static/","public/")
  
  generate_pages_recursive("content/", "template.html", "public/")
  
  
if __name__ == "__main__":
  main()