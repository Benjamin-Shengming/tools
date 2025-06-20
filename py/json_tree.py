#! /usr/bin/env python3

'''
show json  as tree in rich tree with panel 
each panel contains properties of the json object 
and some key words lick children  indicate the children of the object 
and will be show as child of the node
'''
import typer  
import json
from pathlib import Path
from typing import List, Dict
from qutil.log.log import setup_logger
from loguru import logger
from cryptography import x509
from cryptography.x509 import load_pem_x509_certificates, load_der_x509_certificate
from rich.tree import Tree
from rich.panel import Panel
from rich.console import Console

app = typer.Typer()


def build_rich_tree(data, child_key='children', title_key='name'):
    """
    Recursively build a rich Tree from a JSON-like dict/list.
    Each node is a Panel with the object's properties (except children).
    Children are shown as subnodes.
    """
    if isinstance(data, dict):
        # Separate children and other properties
        children = data.get(child_key, [])
        props = {k: v for k, v in data.items() if k != child_key and k != title_key}
        panel_title = data.get(title_key) or 'Object'
        panel = Panel(str(props), title=panel_title, expand=False)
        node = Tree(panel, guide_style="bold bright_blue")
        for child in children:
            node.add(build_rich_tree(child, child_key=child_key, title_key=title_key))
        return node
    elif isinstance(data, list):
        node = Tree('List', guide_style="bold bright_blue")
        for item in data:
            node.add(build_rich_tree(item, child_key=child_key, title_key=title_key))
        return node
    else:
        return Tree(repr(data), guide_style="bold bright_blue")


@app.command()
def show(
    json_file: Path = typer.Argument(..., help="Path to the JSON file to display as a tree."),
    child_key: str = typer.Option('children', help="Key to use for children nodes."),
    title_key: str = typer.Option('name', help="Key to use for panel title."),
):
    """
    Show a JSON file as a forest using rich Panel and Tree.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    console = Console()
    # If the root is a list, show each as a separate tree
    if isinstance(data, list):
        for idx, item in enumerate(data):
            tree = build_rich_tree(item, child_key=child_key, title_key=title_key)
            console.print(tree)
    else:
        tree = build_rich_tree(data, child_key=child_key, title_key=title_key)
        console.print(tree)

if __name__ == "__main__":
    app()



