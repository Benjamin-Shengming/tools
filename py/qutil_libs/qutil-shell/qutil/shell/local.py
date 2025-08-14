import os
from contextlib import contextmanager
from loguru import logger
from invoke.watchers import Responder
import invoke

# Context manager to temporarily set environment variables
@contextmanager
def environ(new_env: dict):
    """
    Temporarily set environment variables inside the context.
    Restores the original environment after exiting the block.
    """
    old_env = os.environ.copy()
    try:
        if new_env:
            os.environ.update(new_env)
        logger.debug(f"Env variables: {os.environ}")
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)
        logger.debug(f"Restored Env variables: {os.environ}")

@contextmanager
def cwd(path):
    old_cwd = os.getcwd()
    try:
        os.chdir(path)
        logger.debug(f"Changed working directory to: {path}")
        yield
    finally:
        os.chdir(old_cwd)
        logger.debug(f"Restored working directory to: {old_cwd}")

def run(command: str, 
    responses: dict = {}, 
    hide=True, 
    warn=False, 
    pty=True,
    return_as_str = False,
    environment: dict = None) ->str|dict: 
    """
    Runs a local shell command and responds to prompts using regex patterns.

    Parameters:
    command (str): The shell command to run.
    responses (dict): Dict where keys are regex patterns and values are responses.
    hide (bool): If True, hides output during execution.
    warn (bool): If True, does not raise on non-zero exit codes.
    environment (dict): Environment variables to set for the command.

    Returns:
    dict: { 'stdout': str, 'stderr': str, 'exit_code': int }
    """

    watchers = [
        Responder(
            pattern=pattern,
            response=(
                response + "\n" if not response.endswith("\n") else response
            ),
        )
        for pattern, response in responses.items()
    ]

    logger.debug(f"Running command: {command}")
    result = invoke.run(
        command, watchers=watchers, hide=hide, warn=warn, pty=pty, env=environment
    )

    if return_as_str:
        return result.stdout + result.stderr
    else:
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.exited,
        }
