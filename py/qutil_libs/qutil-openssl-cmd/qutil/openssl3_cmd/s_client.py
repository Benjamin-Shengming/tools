from typing import List, Optional, Tuple
from qutil.shell.local import run as shell_run

class SClient:
    def __init__(self, openssl_bin: str = "openssl"):
        self.openssl_bin = openssl_bin

    def run(self, host: str, port: int = 443, options: Optional[List[str]] = None, input_data: Optional[str] = None, timeout: Optional[int] = 10) -> dict:
        """
        Run openssl s_client with arbitrary options.

        Parameters:
            host (str): The target host to connect to.
            port (int): The port to connect to (default: 443).
            options (Optional[List[str]]): List of additional s_client options (e.g., ['-CAfile', 'ca.pem', '-verify', '5']).
            input_data (Optional[str]): Data to send to stdin of the process.
            timeout (Optional[int]): Timeout in seconds (not currently enforced by shell_run).

        Returns:
            dict: { 'stdout': str, 'stderr': str, 'exit_code': int }
        """
        cmd = [self.openssl_bin, "s_client", "-connect", f"{host}:{port}"]
        if options:
            cmd.extend(options)
        cmd_str = " ".join(cmd)
        return shell_run(cmd_str, return_as_str=False)
