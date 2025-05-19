from loguru import logger
from invoke.watchers import Responder
import invoke


def run(command: str, responses: dict = {}, hide=True, warn=False, pty=True):
    """
    Runs a local shell command and responds to prompts using regex patterns.

    Parameters:
    command (str): The shell command to run.
    responses (dict): Dict where keys are regex patterns and values are responses.
    hide (bool): If True, hides output during execution.
    warn (bool): If True, does not raise on non-zero exit codes.

    Returns:
    dict: { 'stdout': str, 'stderr': str, 'exit_code': int }
    """

    watchers = [Responder(pattern=pattern, response=response + "\n" if not response.endswith("\n") else response)
                for pattern, response in responses.items()]

    logger.debug(f"Running command: {command}")
    result = invoke.run(command,
                        watchers=watchers,
                        hide=hide,
                        warn=warn,
                        pty=pty)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exited

    }
