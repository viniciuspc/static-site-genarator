import os

from functions.markdown_to_html_node import markdown_to_html_node
from functions.extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
  abs_from_path = os.path.abspath(from_path)
  abs_template_path = os.path.abspath(template_path)
  abs_dest_path = os.path.abspath(dest_path)
  
  print(f"Generating page from [{abs_from_path}] to [{abs_dest_path}] using [{abs_template_path}]")
  
  markdown = ""
  with open(abs_from_path, "+r") as f:
    markdown = f.read()
    
  template = ""
  with open(abs_template_path, "+r") as f:
    template = f.read()
    
  content = markdown_to_html_node(markdown).to_html()
  title = extract_title(markdown)
  
  final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
  
  abs_dest_dir = os.path.join("/",*abs_dest_path.split("/")[0:-1])
  print(abs_dest_dir)
  os.makedirs(abs_dest_dir, exist_ok=True)
  
  with open(abs_dest_path, "+w") as f:
    f.write(final_html)
  