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
  
class LeafNode(HTMLNode):
  def __init__(self, value, tag=None, props=None):
    super().__init__(tag=tag, value=value, props=props)
    
  def to_html(self):
    if self.value is None:
      print(self)
      raise ValueError("All leaf nodes must have a value.")
    
    if not self.tag:
      return self.value
    
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def __repr__(self):
    return f"LeafNode(Tag: |{self.tag}|, Value: |{self.value}|, Props: |{self.props_to_html()}|)"
  
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag=tag, children=children, props=props)
    
  def to_html(self):
    if not self.tag:
      raise ValueError("All parent nodes must have a tag.")
    
    if not self.children:
      raise ValueError("All parent nodes must have children.")
    
    child_html = ""
    
    for child in self.children:
      child_html = f"{child_html}{child.to_html()}"
      
    return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"