import re

def extract_title(markdown):
  matches = re.findall(r"(?m)^\s*#\s+(?!#)(.+?)\s*$", markdown)
  if len(matches) == 0:
    raise Exception("No title found in the markdown")
  
  title = matches[0]
  return title