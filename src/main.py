import sys

from functions.copy_tree import copy_tree
from functions.generate_pages_recursive import generate_pages_recursive
def main():
  if len(sys.argv) < 2:
        print("Usage: python3 main.py <basepath>")
        sys.exit(1)
  else:
    basepath = sys.argv[1]
    
    copy_tree("static/","docs/")
    
    generate_pages_recursive("content/", "template.html", "docs/", basepath)
  
  
if __name__ == "__main__":
  main()