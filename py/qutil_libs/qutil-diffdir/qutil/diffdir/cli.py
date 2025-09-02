import typer
from pathlib import Path
from typing import List
from .diff import diffs, to_html

from rich.table import Table
from rich.console import Console

def to_rich_table(diff_result, folders):
    """
    Render the diff result as a Rich table.
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("File")
    for folder in folders:
        table.add_column(str(folder))
    for row in diff_result:
        values = [row["file"]] + [str(row.get(str(folder), None)) for folder in folders]
        table.add_row(*values)
    return table

app = typer.Typer()


@app.command()
def show_diffs(
    folders: List[Path],
    output: Path = typer.Option("./diff.html", help="Output HTML file for the diff table"),
    file_exts: List[str] = typer.Option(None, help="Only compare files with these extensions, e.g. .py .txt"),
    exclude_rep_path: List[str] = typer.Option(None, help="Ignore all files under these relative paths (prefix match)")
):
    """Show diffs of files under the given folders in a table, and optionally output to HTML."""
    if len(folders) < 2:
        typer.echo("Please provide at least two folders.")
        raise typer.Exit(1)

    result = diffs(folders, file_exts=file_exts, exclude_rep_path=exclude_rep_path)

    if not result:
        typer.echo("No differences found.")
        raise typer.Exit(0)

    table = to_rich_table(result, folders)
    console = Console()
    console.print(table)

    if output:
        to_html(result, folders, output)
        typer.echo(f"Diff written to {output}")
        return

def main():
    app()
     
     
if __name__ == "__main__":
    main()
