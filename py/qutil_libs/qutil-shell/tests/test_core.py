from qutil.shell import local
 
def test_hello():
  local.run("echo hello")

  local.run("ls -lah", hide=True, warn=True)