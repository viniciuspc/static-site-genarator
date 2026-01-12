from functions.copy_tree import copy_tree
def main():
  copy_tree("static/","public/")
  
  
if __name__ == "__main__":
  main()