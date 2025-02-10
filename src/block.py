import re
from enum import Enum

class BlockType(Enum):
    CODE = "code"
    HEADING = "heading"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"

def markdown_to_blocks(markdown):
    md_blocks = []
    if markdown:
        blocks = markdown.split("\n\n")
        for block in blocks:
            stripped = block.strip().strip("\n")
            if stripped:
                md_blocks.append(stripped)
    return md_blocks


def block_to_block_type(block_of_markdown):
    
    pattern = r"^#{1,6}"
    if re.findall(pattern, block_of_markdown):return BlockType.HEADING

    pattern = r"^```[\s\S]*```$"
    if re.findall(pattern, block_of_markdown):return BlockType.CODE

    pattern = r"^(>.*\n)*>.*$"
    if re.findall(pattern, block_of_markdown):return BlockType.QUOTE

    pattern = r"^([\*-] .*\n)*[\*-] .*$"
    if re.findall(pattern, block_of_markdown, re.MULTILINE):return BlockType.UNORDERED_LIST

    # Last check, if this fails => default or paragraph
    pattern = r"^(1\. .*\n|(\d+)\.\s.*\n)*\d\.\s.*$"    # Check for 'N. ' at the start of each line; including the last if empty"
    if re.findall(pattern, block_of_markdown, re.MULTILINE):
        lines = block_of_markdown.splitlines()          # Check for sequential numbers starting at 1
        if lines:
            for i, line in enumerate(lines, start=1):
                if not re.match(rf"^{i}\. .+", line):  # Check if each line matches the number
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH  # Failed all type checks => default to paragraph

