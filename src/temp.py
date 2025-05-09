from textnode import TextType, TextNode
import re


def process_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        splits = old_node.text.split(delimiter)
        if len(splits) < 3:
            result.append(old_node)
            continue

        for i in range(len(splits)):
            if i == 0:
                if splits[i]:
                    result.append(TextNode(splits[i], TextType.TEXT))
            elif i % 2 == 1:
                # This is content between delimiters
                result.append(TextNode(splits[i], text_type))
            else:
                if splits[i]:
                    result.append(TextNode(splits[i], TextType.TEXT))

    return result


def process_links(old_nodes):
    result = []
    link_regex = r"\[(.*?)\]\((.*?)\)"

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        matches = re.finditer(link_regex, old_node.text)
        last_end = 0
        has_match = False

        for match in matches:
            has_match = True
            start, end = match.span()

            if start > last_end:
                result.append(TextNode(old_node.text[last_end:start], TextType.TEXT))

            text = match.group(1)
            result.append(TextNode(text, TextType.LINK))
            last_end = end

        if not has_match:
            result.append(old_node)
        elif last_end < len(old_node.text):
            result.append(TextNode(old_node.text[last_end:], TextType.TEXT))

    return result


def process_images(old_nodes):
    result = []
    image_regex = r"!\[(.*?)\]\((.*?)\)"

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        matches = re.finditer(image_regex, old_node.text)
        last_end = 0
        has_match = False

        for match in matches:
            has_match = True
            start, end = match.span()

            if start > last_end:
                result.append(TextNode(old_node.text[last_end:start], TextType.TEXT))

            alt_text = match.group(1)
            result.append(TextNode(alt_text, TextType.IMAGE))
            last_end = end

        if not has_match:
            result.append(old_node)
        elif last_end < len(old_node.text):
            result.append(TextNode(old_node.text[last_end:], TextType.TEXT))

    return result
