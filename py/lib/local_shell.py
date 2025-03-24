import subprocess

def run_cmd(command, log=None):
    """
    Runs a shell command and returns the result as a string.
    
    :param command: The shell command to run.
    :type command: str
    :return: The result of the shell command.
    :rtype: str
    """
    result = subprocess.run(command, 
                            shell=True, 
                            capture_output=True, 
                            text=True)
    if log:
        if result.returncode != 0:
            log.fail(command)
        else:
            log.success(command) 
    return result.stdout.strip()

# Example usage
if __name__ == "__main__":
    from color_print import ColorPrint
    log = ColorPrint()
    print(run_cmd('ls -l', log=log))
