import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


class TestFunctions(unittest.TestCase):

    def test_text(self):
        text = "Sample text"
        result = "Sample text"
        node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.to_html(), result)

    def test_bold(self):
        tag = "b"
        text = "Sample text"
        result = f"<{tag}>{text}</{tag}>"
        node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.to_html(), result)

    def test_italic(self):
        tag = "i"
        text = "Sample text"
        result = f"<{tag}>{text}</{tag}>"
        node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.to_html(), result)

    def test_code(self):
        tag = "code"
        text = "Sample text"
        result = f"<{tag}>{text}</{tag}>"
        node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.to_html(), result)

    def test_link(self):
        tag = "a"
        text = "Sample text"
        url = "http://example.com"
        result = f'<{tag} href="{url}">{text}</{tag}>'
        node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.to_html(), result)

    def test_image(self):
        tag = "img"
        text = "Sample text"
        url = "http://example.com"
        result = f'<{tag} src="{url}">{text}</{tag}>'
        node = TextNode(text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, tag)
        self.assertEqual(html_node.to_html(), result)


if __name__ == "__main__":
    unittest.main()
