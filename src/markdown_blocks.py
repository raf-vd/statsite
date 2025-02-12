import re
import itertools
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")         # Each block is delimited by an empty line
    filtered_blocks = []
    for block in blocks:
        if block == "":                     # Filter out any excess empty lines
            continue
        block = block.strip()               # Remove any leading/trailing whitespace
        filtered_blocks.append(block)       
    return filtered_blocks

def block_to_block_type(block_of_markdown):
    
    pattern = r"^#{1,6}"
    if re.findall(pattern, block_of_markdown):return block_type_heading

    pattern = r"^```[\s\S]*```$"
    if re.findall(pattern, block_of_markdown):return block_type_code

    pattern = r"^(> .*\n)*>.*$"
    if re.findall(pattern, block_of_markdown):return block_type_quote

    pattern = r"^([\*-] .*\n)*[\*-] .*$"
    if re.findall(pattern, block_of_markdown, re.MULTILINE):return "unordered_list"

    # Last check, if this fails => default or paragraph
    pattern = r"^(1\. .*\n|(\d+)\.\s.*\n)*\d\.\s.*$"    # Check for 'N. ' at the start of each line; including the last if empty"
    if re.findall(pattern, block_of_markdown, re.MULTILINE):
        lines = block_of_markdown.splitlines()          # Check for sequential numbers starting at 1
        if lines:
            for i, line in enumerate(lines, start=1):
                if not re.match(rf"^{i}\. .+", line):  # Check if each line matches the number
                    return block_type_paragraph
            return block_type_olist
    
    return block_type_paragraph  # Failed all type checks => default to paragraph

def get_heading(text):
    count = sum(1 for _ in itertools.takewhile(lambda c: c == "#", text))   # Get number of consecutive # at the beginning of the text
    if count == 0: raise ValueError("This is not a valid heading")          # No heading tag found
    if count > 6: count = 6                                                 # 6# is max, rest is literal text
    return f"h{count}", text[count+1:]                                      # Return the corresponding HTML tag based on the count

def markdown_to_html_node(markdown):
    nodes_out = []                                          
    blocks = markdown_to_blocks(markdown)                   # Split markdown text into blocks

    # Loop each block
    for block in blocks:
        
        textnodes = []
        nest = ""                                           # Default to no nesting
        block_type = block_to_block_type(block)             # Determine block type
        
        if block_type == block_type_heading:                # Handle heading block
            tag, text = get_heading(block)                  
        elif block_type == block_type_code:                 # Handle code block
            tag = "code"
            text = block[3:-3]
            nest = "pre"                                    # Nest code blocks in pre tag
        elif block_type == block_type_quote:                # Handle quote block
            tag = "blockquote"
            text = remove_line_leadchars(block, " ")        # Remove > from start of each line
        elif block_type == block_type_ulist:                # Handle unordered list
            tag = "ul"
            text = remove_line_leadchars(block, " ")        # Remove bullets from start of each line
            text = include_line_in_tag(text,"li")           # Add li tag on each line
        elif block_type == block_type_olist:                # Handle ordered list
            tag = "ol"
            text = remove_line_leadchars(block, " ")        # Remove numbers from start of each line
            text = include_line_in_tag(text,"li")           # Add li tag on each line
        else:                                               # Default: handle paragraph block
            tag = "p"                                                                      
            text = block

        textnodes = text_to_textnodes(text)                                                 # Convert to textnodes
        nodes_out.append(ParentNode(tag, textnodes_to_children(textnodes, nest)))           # Block level ParentNode with children (nested in <pre>)

    nodes_out = ParentNode("div", nodes_out)                # Nest all blocks in <div> parent
    # nodes_out = ParentNode("html",nodes_out)                # Return all noes nested in 1 final (html) ParentNode
    return nodes_out                                        

def textnodes_to_children(textnodes, nest=""):              # Convert each TextNode to an HTMLNode
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))       # Add HTMLNode to outputlist
    if nest:                    
        children = [ParentNode(nest, children)]             # Nest if needed (code block is nested in pre(ParentNode))
    return children

def remove_line_leadchars(block, char):
    lines = block.splitlines()                                                  # Split block in line
    cleaned_lines = list(map(lambda line: line[line.find(char) + 1:], lines))   # Remove text up an until 'char' from each linestart
    return "\n".join(cleaned_lines)                                             # Return cleaned lines joined to blocl again

def include_line_in_tag(block, tag):
    lines = block.splitlines()                                                  # Split block in line
    tagged_lines = list(map(lambda line: f"<{tag}>{line}</{tag}>", lines))      # Put opening and closing tag on each line
    return "\n".join(tagged_lines)                                              # Return tagged lines joined to blocl again


# md="""# This **is** a heading

# ```This is *some* code in a paragraph.
# It spans 2 lines and has a `codeword` in it.```

# This is a paragraph of text. It has some **bold** and *italic* words inside of it.

# > You can quote me all you like.
# > Even in **2** lines.
# > Funny, isn't it?

# * This is the first list item in a list block
# * This is a list item with a bold word at the **end**
# * This is another list item

# 1. Now for an ordered list
# 2. Just 3 lines to start
# 3. Link in ordered list [link](https://www.google.com)

# Finally a closing word:
# THIS IS THE END!
# """

# md = """
# ```
# This is a code block
# ```

# this is paragraph text

# """
# html_final = markdown_to_html_node(md)
# print(html_final.to_html())


