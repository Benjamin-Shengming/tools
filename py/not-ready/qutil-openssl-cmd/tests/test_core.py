
from qutil.openssl3_cmd import openssl3
from qutil.log.log import setup_logger

setup_logger(console_log=True, level="DEBUG")

def test_hello():
    ret = openssl3.run("echo hello")
    assert isinstance(ret, dict)
    assert ret["stdout"].strip() == "hello"

    ret = openssl3.run("echo hello", return_as_str=True)
    assert isinstance(ret, str)
    assert ret.strip() == "hello"

    ret = openssl3.run("ls -lah", hide=True, warn=True)
    assert ret["exit_code"] == 0
