from enum import Enum

class TextType(Enum):
    """
    Enum for text types.
    """
    PLAIN = 1
    MARKDOWN = 2
    HTML = 3
    BOLD = 4

class TextNode():
    """
    Class representing a text node.
    """
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(obj1, obj2):
        return isinstance(obj1, TextNode) and obj1.text == obj2.text and obj1.text_type == obj2.text_type and obj1.url == obj2.url

    def __repr__(self):
        return f"TextNode(text={self.text}, text_type={self.text_type}, url={self.url})"
