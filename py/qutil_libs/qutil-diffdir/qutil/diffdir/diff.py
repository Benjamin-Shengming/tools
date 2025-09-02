#!/usr/bin/env python

from pathlib import Path
from hashlib import sha256
from typing import List, Tuple, Generator, Any


def hash_file(f: Path) -> str:
    # return sha256 for f
    h = sha256()
    with open(f, "rb") as file:
        chunk = file.read(8192)
        while chunk:
            h.update(chunk)
            chunk = file.read(8192)
    return h.hexdigest()


def calculate_files_sha256(
    folder_path: Path,
    file_exts: List[str] = None,
    exclude_rep_path: List[str] = None
) -> List[Tuple[Path, str]]:
    """
    Recursively find files, filter by extension and exclude paths, and return (relative_path, sha256).
    """
    ret = []
    for file in folder_path.rglob("*"):
        if file.is_file():
            relative_path = file.relative_to(folder_path)
            # Filter by extension if specified
            if file_exts is not None and len(file_exts) > 0:
                if not any(str(relative_path).endswith(ext) for ext in file_exts):
                    continue
            # Exclude paths if specified
            if exclude_rep_path is not None and len(exclude_rep_path) > 0:
                if any(str(relative_path).startswith(exclude) for exclude in exclude_rep_path):
                    continue
            sha256 = hash_file(file)
            ret.append((relative_path, sha256))
    return ret


def sort_files_sha256(files_sha256: List[Tuple[Path, str]]) -> List[Tuple[Path, str]]:
    """
    Sorts the list of (relative_path, sha256) tuples lexically by relative_path.
    """
    return sorted(files_sha256, key=lambda x: str(x[0]))


def diffs(
    folder_paths: List[Path],
    file_exts: List[str] = None,
    exclude_rep_path: List[str] = None
) -> List[dict]:
    """
    Accepts a list of folder paths (at least 2), finds the diffs of files under all the folders.
    Only compares files with specified extensions and ignores files under exclude_rep_path.
    Returns a list of dicts, each dict has keys as file paths (relative), values as sha256 or None if not present in that folder.
    """
    if len(folder_paths) < 2:
        raise ValueError("At least two folder paths are required.")
    # folder should be different
    if len(set(folder_paths)) < 2:
        raise ValueError("All folder paths must be different.")

    # Collect all file hashes for each folder
    all_hashes = []
    all_files_set = set()
    for folder in folder_paths:
        files_sha256 = calculate_files_sha256(folder, file_exts=file_exts, exclude_rep_path=exclude_rep_path)
        files_dict = {str(rel_path): sha for rel_path, sha in files_sha256}
        all_hashes.append(files_dict)
        all_files_set.update(files_dict.keys())

    # Union of all file paths
    all_files = sorted(all_files_set)

    # Build the result: a list of dicts, one per file, with sha256 or None for each folder
    result = []
    for file in all_files:
        # same file get hashed from different folder
        hashes = [files_dict.get(file, None) for files_dict in all_hashes]
        # Ignore if all hashes are the same (including all None)
        if all(h == hashes[0] for h in hashes):
            continue
        entry = {"file": file}
        for folder, h in zip(folder_paths, hashes):
            entry[str(folder)] = h
        result.append(entry)
    return result


def to_html(
    diff_result: List[dict], folder_paths: List[Path], output_file: Path
) -> None:
    """
    Render the diff result to an HTML file as a table.
    """
    html = []
    html.append('<html><head><meta charset="utf-8"><title>Directory Diff</title>')
    html.append(
        "<style>table {border-collapse: collapse;} th, td {border: 1px solid #ccc; padding: 4px;} th {background: #eee;}</style>"
    )
    html.append("</head><body>")
    html.append("<h2>Directory Diff</h2>")
    html.append("<table>")
    html.append("<tr><th>File</th>")
    for folder in folder_paths:
        html.append(f"<th>{folder}</th>")
    html.append("</tr>")
    for row in diff_result:
        html.append(f'<tr><td>{row["file"]}</td>')
        for folder in folder_paths:
            val = row.get(str(folder), "")
            html.append(f'<td>{val if val is not None else ""}</td>')
        html.append("</tr>")
    html.append("</table></body></html>")
    output_file.write_text("\n".join(html), encoding="utf-8")
