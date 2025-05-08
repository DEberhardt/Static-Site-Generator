import unittest

from functions import split_nodes_delimiter, extract_markdown_images
from textnode import TextType, TextNode


class Testsplit_nodes_delimiter(unittest.TestCase):
    # TBC
    def test_passthru(self):
        old_nodes = [
            TextNode("Sample text", TextType.TEXT),
            TextNode("Sample text", TextType.TEXT),
            TextNode("Sample text", TextType.TEXT),
        ]
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(before, old_nodes)
        self.assertEqual(after, [])

    def test_empty_nodes(self):
        old_nodes = []
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(before, [])
        self.assertEqual(after, [])

    def test_delimiter_at_start(self):
        old_nodes = [
            TextNode("*", TextType.TEXT),
            TextNode("Sample text", TextType.TEXT),
            TextNode("More text", TextType.TEXT),
        ]
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(before, [])
        self.assertEqual(after, [old_nodes[1], old_nodes[2]])

    def test_delimiter_at_end(self):
        old_nodes = [
            TextNode("Sample text", TextType.TEXT),
            TextNode("More text", TextType.TEXT),
            TextNode("*", TextType.TEXT),
        ]
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(before, [old_nodes[0], old_nodes[1]])
        self.assertEqual(after, [])

    def test_delimiter_in_middle(self):
        old_nodes = [
            TextNode("Sample text", TextType.TEXT),
            TextNode("*", TextType.TEXT),
            TextNode("More text", TextType.TEXT),
        ]
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(before, [old_nodes[0]])
        self.assertEqual(after, [old_nodes[2]])

    def test_multiple_delimiters(self):
        old_nodes = [
            TextNode("Sample text", TextType.TEXT),
            TextNode("*", TextType.TEXT),
            TextNode("More text", TextType.TEXT),
            TextNode("*", TextType.TEXT),
            TextNode("Even more", TextType.TEXT),
        ]
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(before, [old_nodes[0]])
        self.assertEqual(after, [old_nodes[2], old_nodes[4]])

    def test_different_node_types(self):
        old_nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("*", TextType.TEXT),
            TextNode("Italic text", TextType.ITALIC),
        ]
        before, after = split_nodes_delimiter(old_nodes, "*", TextType.CODE)
        self.assertEqual(before, [old_nodes[0]])
        self.assertEqual(after, [old_nodes[2]])

class TestExtractMarkdownImages(unittest.TestCase):
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
