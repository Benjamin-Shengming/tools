# Typer CLI for Jira issue fetching
import typer
import yaml
from pathlib import Path
from typing import Optional
from .client import JiraClient
from qutil.log.log import setup_logger

setup_logger(console_log=True, level="DEBUG")

app = typer.Typer()

def load_config(config_path: Path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

@app.command()
def tickets(
    user: Optional[str] = typer.Option(None, help="Jira username"),
    password: Optional[str] = typer.Option(None, help="Jira password"),
    server: Optional[str] = typer.Option(None, help="Jira server URL"),
    jql: Optional[str] = typer.Option(None, help="JQL query string"),
    config: Optional[Path] = typer.Option(None, help="YAML config file with server, user, password, jql")
):
    """Fetch and print Jira tickets one by one."""
    if config:
        cfg = load_config(config)
        user_ = cfg.get('user') or cfg.get('username')
        password_ = cfg.get('password')
        server_ = cfg.get('server')
        jql_ = cfg.get('jql')
    else:
        user_ = user
        password_ = password
        server_ = server
        jql_ = jql
    if not (user_ and password_ and server_ and jql_):
        typer.echo("Error: Must provide user, password, server, and jql (either as options or in config file)")
        raise typer.Exit(1)
    client = JiraClient(server_, user_, password_)
    logger.debug("jql {jql_}")
    for issue in client.iter_issues(jql_):
        typer.echo(f"{issue.key}: {issue.fields.summary}")

def main():
    app()

if __name__ == "__main__":
    main()
