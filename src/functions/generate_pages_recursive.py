import os

from functions.generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
  for content in os.listdir(dir_path_content):
    content_path = os.path.join(dir_path_content, content)
    dest_content_path = os.path.join(dest_dir_path, content.replace(".md", ".html"))
    is_file = os.path.isfile(content_path)
    
    if is_file:
      generate_page(content_path, template_path, dest_content_path, basepath)
      #print(f"{content_path} ----> {dest_content_path}")
    else:
      generate_pages_recursive(content_path, template_path, dest_content_path, basepath)