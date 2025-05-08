import unittest

from functions import split_nodes_delimiter
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
