from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
import re
from enum import Enum
from inline import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block[0].isdigit() and block.startswith(". ", 1): # Check for "1. ", "2. ", etc.
        if len(block.split("\n")) > 1: 
            lines = block.split("\n") 
            for i, line in enumerate(lines):
                expected_number = i + 1 
                if not line.startswith(f"{expected_number}. "): 
                    return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    splitblocks = markdown.split("\n\n")
    blocks = []
    for block in splitblocks:
        if block.strip() != "":
            blocks.append(block.strip())
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlnodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                htmlnodes.append(heading_to_html_node(block))
            case BlockType.PARAGRAPH:
                htmlnodes.append(paragraph_to_html_node(block))
            case BlockType.ORDERED_LIST:
                htmlnodes.append(ordered_list_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                htmlnodes.append(unordered_list_to_html_node(block))
            case BlockType.CODE:
                htmlnodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                htmlnodes.append(quote_to_html_node(block))
    parent = ParentNode("div", htmlnodes)
    return parent
        
def heading_to_html_node(block):
    children = text_to_children(block.lstrip("#").strip()) # Remove leading # and spaces
    level = len(block) - len(block.lstrip("#")) # Count number of # to determine level
    return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
    block = block.replace("\n", " ") # Combine lines into single line
    block = " ".join(block.split()) # Remove extra spaces
    children = text_to_children(block)
    return ParentNode("p", children)

def ordered_list_to_html_node(block):
    items = block.split("\n") # Each line is a list item
    li_nodes = []
    for item in items:
        children = text_to_children(item[item.index(".")+1:].strip()) # Remove number and dot
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)

def unordered_list_to_html_node(block):
    items = block.split("\n") # Each line is a list item
    li_nodes = []
    for item in items:
        children = text_to_children(item[2:].strip())
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)

def code_to_html_node(block):
    content = block[4:-3] # Remove ``` and newlines
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, content)])])

def quote_to_html_node(block):
    children = []
    recombined = ""
    for line in block.split("\n"):
        if line.startswith(">"):
            content = line[1:].strip() # Remove > and leading spaces
            recombined += content + " " # Recombine lines with space
    children = text_to_children(recombined.strip())     
    return ParentNode("blockquote", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text) 
    html_nodes = [text_node_to_html_node(tn) for tn in text_nodes] 
    return html_nodes
