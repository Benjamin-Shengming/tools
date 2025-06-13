#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import tarfile
import hashlib
import tempfile
import typer
from pathlib import Path
from typing import List, Dict
import shutil
import os
from qutil.log.log import setup_logger
from loguru import logger
from rich.table import Table
from rich.console import Console

app = typer.Typer()

def sha256sum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def extract_tar_to_temp(tar_path: Path) -> Path:
    """Extract a tar file to a temporary directory."""
    temp_dir = tempfile.mkdtemp(prefix=f"{tar_path.stem}_")
    logger.info(f"Extracting tar file: {tar_path} to {temp_dir}")
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(temp_dir)
    return Path(temp_dir)

def is_tar_extractable(path: Path) -> bool:
    """Check if the file is a valid tar file."""
    try:
        with tarfile.open(path, 'r') as tar:
            return True
    except (tarfile.TarError, OSError):
        return False  
  
def get_dir_file_hashes(dir_path: Path, ignore_top_folder: bool = False) -> Dict[str, str]:
    """Get {relative_path: sha256 hash} for files in a directory.
    If ignore_top_folder is True, strip the first path component."""
    hashes = {}
    # If ignoring top folder, find the single top-level directory
    base_path = dir_path
    if ignore_top_folder:
        entries = [p for p in dir_path.iterdir() if p.is_dir()]
        if len(entries) == 1:
            base_path = entries[0]
    for path in base_path.rglob('*'):
        if path.is_file():
            rel_path = path.relative_to(base_path).as_posix()
            content = path.read_bytes()
            hashes[rel_path] = sha256sum(content)
            logger.debug(f"File: {rel_path}, Hash: {hashes[rel_path]}")
    return hashes

@app.command()
def compare(sources: List[Path]):
    """
    Compare multiple folders or tar files.
    Tar files will be extracted to temp folders first.
    Only files that differ or are missing are reported.
    """
    console = Console()
    console.print(f"Comparing {len(sources)} sources...")
    temp_dirs = []
    content_map = {}

    try:
        for source in sources:
            console.print(f"Processing: {source}")
            if source.is_file() and is_tar_extractable(source):
                temp_dir = extract_tar_to_temp(source)
                temp_dirs.append(temp_dir)
                content_map[source] = get_dir_file_hashes(temp_dir, ignore_top_folder=True)
            elif source.is_dir():
                content_map[source] = get_dir_file_hashes(source)
            else:
                console.print(f"[yellow]⚠️ Skipping unsupported source: {source}[/yellow]")

        # Collect union of all relative file paths
        all_files = set()
        for hashes in content_map.values():
            all_files.update(hashes.keys())

        # Prepare rich table
        table = Table(title="Diff or Missing Files")
        table.add_column("File Path", style="bold")
        for src in content_map.keys():
            # Show only the base name of the source (ignore root folder path)
            table.add_column(src.name, overflow="fold")

        for file_path in sorted(all_files):
            file_hashes = set()
            row = [file_path]
            for src, files in content_map.items():
                h = files.get(file_path)
                if h:
                    row.append(h[:12])
                    file_hashes.add(h)
                else:
                    row.append("[red]MISSING[/red]")
            if len(file_hashes) > 1 or row.count("[red]MISSING[/red]") > 0:
                table.add_row(*row)

        if table.row_count:
            console.print(table)
        else:
            console.print("[green]No differences found![/green]")

    finally:
        for temp in temp_dirs:
            shutil.rmtree(temp)

@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging")
):
    typer.echo("Starting call back...")
    setup_logger(console_log=True, level="DEBUG" if debug else "INFO")
    
if __name__ == "__main__":
    app()
