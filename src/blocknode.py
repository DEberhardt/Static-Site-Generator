# from htmlnode import LeafNode
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDEREDLIST = "unordered_list"
    ORDEREDLIST = "ordered_list"

def block_to_block_type(block):
    """
    Converts a block to its corresponding BlockType.

    Args:
        block (str): The block to convert.

    Returns:
        BlockType: The converted BlockType.
    """
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith(("- ")):
        marker = "- " if block.startswith("- ") else "* "
        for line in lines:
            if not line.startswith(marker):
                return BlockType.PARAGRAPH
        return BlockType.UNORDEREDLIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDEREDLIST
    return BlockType.PARAGRAPH
