import unittest

from functions import *
from textnode import TextType, TextNode


class TestsplitNodesDelimiter(unittest.TestCase):
    # TBC
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
            TextNode("This is _italic_ text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text")
        self.assertEqual(new_nodes[4].text, "This is _italic_ text")

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [
            TextNode("This is plain text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[1].text, "Some text")

    def test_split_nodes_delimiter_empty_list(self):
        old_nodes = []
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 0)

    def test_split_nodes_delimiter_mixed_types(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
            TextNode("This is _italic_ text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text")
        self.assertEqual(new_nodes[4].text, "This is _italic_ text")
        self.assertEqual(new_nodes[5].text, "Bold text")

    def test_split_nodes_delimiter_with_other_types(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
            TextNode("This is _italic_ text", TextType.TEXT),
            TextNode("Code block", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text")
        self.assertEqual(new_nodes[4].text, "This is _italic_ text")
        self.assertEqual(new_nodes[5].text, "Code block")

    def test_split_nodes_delimiter_with_mixed_types(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
            TextNode("This is _italic_ text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text")
        self.assertEqual(new_nodes[4].text, "This is _italic_ text")
        self.assertEqual(new_nodes[5].text, "Bold text")

    def test_split_nodes_delimiter_with_special_characters(self):
        old_nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("Some text with special characters: !@#$%^&*()", TextType.TEXT),
            TextNode("This is _italic_ text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text with special characters: !@#$%^&*()")
        self.assertEqual(new_nodes[4].text, "This is _italic_ text")


class TestExtractMarkdownImages(unittest.TestCase):
    # TBC
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_no_images(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "Text with ![first](https://example.com/first.jpg) and ![second](https://example.com/second.png)"
        )
        self.assertListEqual([
            ("first", "https://example.com/first.jpg"),
            ("second", "https://example.com/second.png")
        ], matches)

    def test_image_with_empty_alt_text(self):
        matches = extract_markdown_images("Image with no alt text: ![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_image_with_complex_url(self):
        matches = extract_markdown_images(
            "Image with query params: ![complex](https://example.com/image.jpg?size=large&format=webp)"
        )
        self.assertListEqual([("complex", "https://example.com/image.jpg?size=large&format=webp")], matches)

    def test_image_surrounded_by_text(self):
        matches = extract_markdown_images(
            "Before ![middle](https://example.com/middle.png) After"
        )
        self.assertListEqual([("middle", "https://example.com/middle.png")], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        old_nodes = [
            TextNode("This is ![image](https://example.com/image.png) text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
            TextNode("This is ![another image](https://example.com/another.png) text", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text")
        self.assertEqual(new_nodes[4].text, "This is ")
        self.assertEqual(new_nodes[5].text, "another image")
        self.assertEqual(new_nodes[5].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[6].text, " text")

    def test_split_nodes_image_no_images(self):
        old_nodes = [
            TextNode("This is plain text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[1].text, "Some text")

    def test_split_nodes_image_empty_list(self):
        old_nodes = []
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 0)

    def test_split_nodes_image_with_text(self):
        old_nodes = [
            TextNode("This is ![image](https://example.com/image.png) text", TextType.TEXT),
            TextNode("Another ![image](https://example.com/another.png) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Another ")
        self.assertEqual(new_nodes[4].text, "image")
        self.assertEqual(new_nodes[4].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[5].text, " here")

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        old_nodes = [
            TextNode("This is [link](https://example.com) text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
            TextNode("This is [another link](https://example.com/another) text", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Some text")
        self.assertEqual(new_nodes[4].text, "This is ")
        self.assertEqual(new_nodes[5].text, "another link")
        self.assertEqual(new_nodes[5].text_type, TextType.LINK)
        self.assertEqual(new_nodes[6].text, " text")

    def test_split_nodes_link_no_links(self):
        old_nodes = [
            TextNode("This is plain text", TextType.TEXT),
            TextNode("Some text", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is plain text")
        self.assertEqual(new_nodes[1].text, "Some text")

    def test_split_nodes_link_empty_list(self):
        old_nodes = []
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 0)

    def test_split_nodes_link_with_text(self):
        old_nodes = [
            TextNode("This is [link](https://example.com) text", TextType.TEXT),
            TextNode("Another [link](https://example.com/another) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[3].text, "Another ")
        self.assertEqual(new_nodes[4].text, "link")
        self.assertEqual(new_nodes[4].text_type, TextType.LINK)
        self.assertEqual(new_nodes[5].text, " here")



class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 0)

    def test_text_to_textnodes_no_formatting(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is plain text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_only_bold(self):
        text = "**This is bold**"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is bold")
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_text_to_textnodes_only_italic(self):
        text = "_This is italic_"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is italic")
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)

    def test_text_to_textnodes_only_code(self):
        text = "`This is code`"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is code")
        self.assertEqual(nodes[0].text_type, TextType.CODE)

    def test_text_to_textnodes_only_link(self):
        text = "[This is a link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is a link")
        self.assertEqual(nodes[0].text_type, TextType.LINK)

    def test_text_to_textnodes_only_image(self):
        text = "![This is an image](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is an image")
        self.assertEqual(nodes[0].text_type, TextType.IMAGE)
