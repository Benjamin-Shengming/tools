from qutil.shell.local import run, cwd, environ
from qutil.log.log import setup_logger

setup_logger(console_log=True, level="DEBUG")

def test_hello():
    ret = run("echo hello")
    assert isinstance(ret, dict)
    assert ret["stdout"].strip() == "hello"

    ret = run("echo hello", return_as_str=True)
    assert isinstance(ret, str)
    assert ret.strip() == "hello"

    with cwd("/usr/local"):
        with environ({"LD_LIBRARY_PATH": "/usr/local/lib"}):
            ret = run("echo $LD_LIBRARY_PATH")
            assert ret["stdout"].strip() == "/usr/local/lib"

            ret = run("ls -lah", hide=True, warn=True)
            assert ret["exit_code"] == 0
            print(ret)

    ret = run("ls -lah", hide=True, warn=True)
    assert ret["exit_code"] == 0
    print(ret)
