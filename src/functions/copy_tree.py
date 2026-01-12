import os
from shutil import copy, rmtree

def copy_tree(source, destination):
  source_path = os.path.abspath(source)
  destination_path = os.path.abspath(destination)
  #print(f"source_path: {source_path} >>>> destination_path: {destination_path}")
  
  # Clean and create a new destination path
  rmtree(destination_path, ignore_errors=True)
  os.mkdir(destination_path)
  
  for item in os.listdir(source_path):
    item_path = os.path.join(source_path, item)
    item_destination_path = os.path.join(destination_path, item)
    if os.path.isfile(item_path):
      copy(item_path, item_destination_path)
    else:
      copy_tree(item_path, item_destination_path)
  