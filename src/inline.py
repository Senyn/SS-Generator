from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            new_nodes.append(nodes)
            continue
        split_texts = nodes.text.split(delimiter)
        if len(split_texts) == 1:
            new_nodes.append(TextNode(split_texts[0], TextType.TEXT))
            continue
        elif len(split_texts)%2 == 0:
            raise ValueError("Delimiter split resulted in even number of segments, indicating unmatched delimiters.")
        else:
            for i, text in enumerate(split_texts):
                if i % 2 == 0:
                    if text:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes


def extract_markdown_images(text):
    extracted = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted

def extract_markdown_links(text):
    extracted = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted
    
def split_nodes_images(old_nodes):
    new_nodes = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            new_nodes.append(nodes)
            continue
        splits = extract_markdown_images(nodes.text)
        if len(splits) == 0:
            new_nodes.append(nodes)
            continue
        else:
            current_text = nodes.text
            for alt_text, url in splits:
                current_text = current_text.split(f"![{alt_text}]({url})", 1)
                if current_text[0] != "":
                    new_nodes.append(TextNode(current_text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                current_text = current_text[1]
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            new_nodes.append(nodes)
            continue
        splits = extract_markdown_links(nodes.text)
        if len(splits) == 0:
            new_nodes.append(nodes)
            continue
        else:
            current_text = nodes.text
            for link_text, url in splits:
                current_text = current_text.split(f"[{link_text}]({url})", 1)
                if current_text[0] != "":
                    new_nodes.append(TextNode(current_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                current_text = current_text[1]
            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes            

def text_to_textnodes(text):
    if text == "":
        return []
    filter_code = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE)
    filter_images = split_nodes_images(filter_code)
    filter_links = split_nodes_links(filter_images)
    filter_bold = split_nodes_delimiter(filter_links, "**", TextType.BOLD)
    filter_italic = split_nodes_delimiter(filter_bold, "_", TextType.ITALIC)
    return filter_italic

    