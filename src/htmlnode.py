class HTMLNode():
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
    
  def to_html(self):
    raise NotImplementedError
  
  def props_to_html(self):
    if self.props:
      html_props = ""
      for prop in self.props:
        html_props = f"{html_props} {prop}=\"{self.props[prop]}\""
      return html_props
    else:
      return ""
    
  def __repr__(self):
    return f"HTMLNode(Tag: |{self.tag}|, Value: |{self.value}|, Children: |{self.children}|, Props: |{self.props_to_html()}|)"