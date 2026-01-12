import unittest

from textnode import TextNode, TextType
from blocktype import BlockType
from functions.text_node_to_html_node import text_node_to_html_node
from functions.split_nodes_delimiter import split_nodes_delimiter
from functions.extract_markdown import extract_markdown_images, extract_markdown_links
from functions.slipt_nodes_image import split_nodes_image
from functions.slipt_nodes_link import split_nodes_link
from functions.text_to_textnodes import text_to_textnodes
from functions.markdown_to_blocks import markdown_to_blocks
from functions.block_to_block_type import block_to_block_type
  
class TestFunctions(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.PLAIN)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")
    
  def test_bold(self):
    node = TextNode("This is a bold text node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a bold text node")
    
  def test_italic(self):
    node = TextNode("This is a italic text node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is a italic text node")
    
  def test_code(self):
    node = TextNode("This is a code text node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is a code text node")
    
  def test_link(self):
    node = TextNode("This is a link text node", TextType.LINK, "https://google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is a link text node")
    self.assertEqual(html_node.props, {"href": "https://google.com"})
    
  def test_image(self):
    node = TextNode("This is a image text node", TextType.IMAGE, "https://google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(html_node.props, {"src": "https://google.com", "alt": "This is a image text node"})

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_code(self):
    node = TextNode("This is text with a `code block` word", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
    ]

    self.assertEqual(new_nodes, expected)

  def test_two_code(self):
    node = TextNode("This is text with a `code block` word and `other code block` word", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word and ", TextType.PLAIN),
        TextNode("other code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN)
    ]

    self.assertEqual(new_nodes, expected)

  def test_code_end(self):
    node = TextNode("This is text with a `code block`", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
    ]

    self.assertEqual(new_nodes, expected)

  def test_code_begin(self):
    node = TextNode("`code block` is a code", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("code block", TextType.CODE),
        TextNode(" is a code", TextType.PLAIN),
        
    ]

    self.assertEqual(new_nodes, expected)

  def test_only_code(self):
    node = TextNode("`code block`", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    expected = [
        TextNode("code block", TextType.CODE),
    ]

    self.assertEqual(new_nodes, expected)

  def test_bold(self):
    node = TextNode("Let us see the **code**", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    expected = [
        TextNode("Let us see the ", TextType.PLAIN),
        TextNode("code", TextType.BOLD),
    ]

    self.assertEqual(new_nodes, expected)

  def test_italic(self):
    node = TextNode("_Italy_", TextType.PLAIN)
    new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
    expected = [
        TextNode("Italy", TextType.ITALIC),
    ]

    self.assertEqual(new_nodes, expected)

  def test_multiple_old_nodes(self):
    nodes = [
        TextNode("Let us see the **code**", TextType.PLAIN),
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word and ", TextType.PLAIN),
        TextNode("_Italy_", TextType.PLAIN),
        TextNode("other code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
        TextNode(" OMG an other `code`", TextType.PLAIN)
    ]
    new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    expected = [
        TextNode("Let us see the ", TextType.PLAIN),
        TextNode("code", TextType.BOLD),
        TextNode("This is text with a ", TextType.PLAIN),
        TextNode("code block", TextType.CODE),
        TextNode(" word and ", TextType.PLAIN),
        TextNode("Italy", TextType.ITALIC),
        TextNode("other code block", TextType.CODE),
        TextNode(" word", TextType.PLAIN),
        TextNode(" OMG an other ", TextType.PLAIN),
        TextNode("code", TextType.CODE),
    ]

    self.assertEqual(new_nodes, expected)

class TestExtractMarkdown(unittest.TestCase):
  def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
  
  def test_extract_markdown_multiple_images(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    
    expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    
    self.assertEqual(extract_markdown_images(text), expected)

  def test_extract_link(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    self.assertEqual(extract_markdown_links(text), expected)

class TestSplitNodesImage(unittest.TestCase):
  def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

  def test_split_only_images(self):
    node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

  def test_split_images_beginning(self):
    node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) what image was that?",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
          TextNode(" what image was that?", TextType.PLAIN),
        ],
        new_nodes,
    )

  def test_split_images_end(self):
    node = TextNode(
        "This is a image ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
          TextNode("This is a image ", TextType.PLAIN),
          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
        ],
        new_nodes,
    )

  def test_split_images_multiple_nodes(self):
    nodes = [TextNode(
          "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
          TextType.PLAIN,
        ),
          TextNode(
          "![image](https://i.imgur.com/zjjcJKZ.png) what image was that?",
          TextType.PLAIN,
        ),
          TextNode(
          "This is a image ![image](https://i.imgur.com/zjjcJKZ.png)",
          TextType.PLAIN,
        )
      ]
    new_nodes = split_nodes_image(nodes)
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.PLAIN),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" what image was that?", TextType.PLAIN),
            TextNode("This is a image ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes,
    )

  def test_split_image_malformated(self):
    node = TextNode(
        "This is a image image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
          TextNode(
          "This is a image image](https://i.imgur.com/zjjcJKZ.png)",
          TextType.PLAIN,)
        ],
        new_nodes,
    )

class TestSplitNodesLink(unittest.TestCase):
  def test_split_links(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
          TextNode("This is text with a link ", TextType.PLAIN),
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
          TextNode(" and ", TextType.PLAIN),
          TextNode(
              "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
          ),
      ],
      new_nodes
    )

  def test_split_only_links(self):
    node = TextNode(
        "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
          TextNode(
              "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
          ),
      ],
      new_nodes
    )

  def test_split_links_beginning(self):
    node = TextNode(
        "[to boot dev](https://www.boot.dev) what link was that?",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
          TextNode(" what link was that?", TextType.PLAIN),
      ],
      new_nodes
    )

  def test_split_links_end(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
          TextNode("This is text with a link ", TextType.PLAIN),
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
      ],
      new_nodes
    )

  def test_split_links_multiple_nodes(self):
    nodes = [TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
    ),
      TextNode(
        "[to boot dev](https://www.boot.dev) what link was that?",
        TextType.PLAIN,
    )
    ]
    new_nodes = split_nodes_link(nodes)
    self.assertListEqual(
      [
          TextNode("This is text with a link ", TextType.PLAIN),
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
          TextNode(" and ", TextType.PLAIN),
          TextNode(
              "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
          ),
          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
          TextNode(" what link was that?", TextType.PLAIN),
      ],
      new_nodes
    )

  def test_split_malformerd_links(self):
    node = TextNode(
        "This is text with a link to boot dev](https://www.boot.dev)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
         TextNode(
        "This is text with a link to boot dev](https://www.boot.dev)",
        TextType.PLAIN,
    )
      ],
      new_nodes
    )

class TestTextToTextnodes(unittest.TestCase):
  def test_text_to_textnodes(self):
    nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    
    self.assertListEqual(
          [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
          ],
          nodes
    )

  def test_text_to_textnodes_end_text(self):
    nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev). Nice!")
    
    self.assertListEqual(
          [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(". Nice!", TextType.PLAIN),
          ],
          nodes
    )
    
class TestMarkdownToBlocks(unittest.TestCase):
      def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
        def test_markdown_to_blocks_multiple_line_bracks(self):
          md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
          blocks = markdown_to_blocks(md)
          self.assertEqual(
              blocks,
              [
                  "This is **bolded** paragraph",
                  "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                  "- This is a list\n- with items",
              ],
          )

class TestBlockToBlockType(unittest.TestCase):
  def test_heading(self):
    block = "# This is a heading"
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.HEADING)
    
  def test_code(self):
    block = """
```
This is a code block
code here
more code
```
"""
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.CODE)
    
  def test_code_empty(self):
    block = """
```
```
"""
    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.CODE)
    
  def test_quote(self):
    block = """
> This is a
> quote    
"""

    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.QUOTE)
    
  def test_unordered_list(self):
    block = """
- This is an
- unordered
- list    
"""

    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
  def test_ordered_list(self):
    block = """
1. This is an
2. unordered
3. list    
"""

    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
  def test_paragraph(self):
    block = """
This is just a 1 pargraph -  
"""

    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.PARAGRAPH)
    
  def test_paragraph_like_list(self):
    block = """
- This is just a 1 
- pargraph
> with
4. other lines  
"""

    block_type = block_to_block_type(block)
    self.assertEqual(block_type, BlockType.PARAGRAPH)
  
    
    
if __name__ == "__main__":
    unittest.main()