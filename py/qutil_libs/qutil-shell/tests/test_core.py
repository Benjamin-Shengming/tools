from qutil.shell import local
from qutil.log.log import setup_logger

setup_logger(console_log=True, level="DEBUG")

def test_hello():
    ret = local.run("echo hello")
    assert isinstance(ret, dict)
    assert ret["stdout"].strip() == "hello"

    ret = local.run("echo hello", return_as_str=True)
    assert isinstance(ret, str)
    assert ret.strip() == "hello"

    ret = local.run("ls -lah", hide=True, warn=True)
    assert ret["exit_code"] == 0
