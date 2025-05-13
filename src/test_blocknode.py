import unittest

# from functions import *
from textnode import *
from blocknode import *
from htmlnode import *
from functions import *

import re

class TestBlockNode(unittest.TestCase):
    """
    Unit tests for the block_to_block_type function in the blocknode module.
    """
    def test_block_to_block_type_paragraph(self):
        # Test for paragraph
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        # Test for paragraph with only whitespace
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        # Test for heading
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        # Test for code block
        # Test for code block with Python
        self.assertEqual(block_to_block_type("```python\nprint('Hello, World!')\n```"), BlockType.CODE)
        # Test for code block with JavaScript
        self.assertEqual(block_to_block_type("```javascript\nconsole.log('Hello, World!');\n```"), BlockType.CODE)
        # Test for code block without language specified
        self.assertEqual(block_to_block_type("```\nNo language specified\n```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        # Test for quote
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_block_to_block_type_list_unordered(self):
        # Test for unordered list with '*'
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDEREDLIST)

    def test_block_to_block_type_list_ordered_basic(self):
        # Test for ordered list
        block = "1. list\n2. items\n3. here"
        self.assertEqual(block_to_block_type(block), BlockType.ORDEREDLIST)

    def test_block_to_block_type_list_ordered_tenplus(self):
        # Test for multi-digit ordered list
        block = "1. list\n2. items\n3. here\n4. done\n5. bye\n6. bye\n7. bye\n8. bye\n9. bye\n10. bye\n11. bye"
        self.assertEqual(block_to_block_type(block), BlockType.ORDEREDLIST)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
