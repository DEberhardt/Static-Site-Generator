from textnode import TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits a list of nodes into two lists based on a delimiter.

    Args:
        old_nodes (list): The list of nodes to split.
        delimiter (str): The delimiter to split the nodes by.
        text_type (TextType): The type of text for the new nodes.

    Returns:
        tuple: A tuple containing two lists: the first with nodes before the delimiter,
               and the second with nodes after the delimiter.
    """
    before_delimiter = []
    after_delimiter = []
    found_delimiter = False

    for node in old_nodes:
        if node.text == delimiter:
            found_delimiter = True
            continue
        if not found_delimiter:
            before_delimiter.append(node)
        else:
            after_delimiter.append(node)

    if not found_delimiter:
        return old_nodes, []

    return before_delimiter, after_delimiter

def extract_markdown_images(text):
    """
    Extracts markdown images from a given text.

    Args:
        text (str): The input text containing markdown images.

    Returns:
        list: A list of tuples containing the image URL and alt text.
    """
    import re

    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]
