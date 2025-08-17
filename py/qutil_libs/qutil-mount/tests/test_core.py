from qutil.mount.mount import cifs, sshfs
from qutil.log.log import setup_logger
from qutil.shell.local import run
import os

setup_logger(console_log=True, level="DEBUG")

qdrive_ip = "192.168.10.8"
svn_user = "buildbot"
svn_pass = "Ortomag1c"
q_drive_path = f"/Shared-Data/Buildbot"

def is_empty(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if dirs or files:
            return False
    return True

def test_cifs_mount():
    mount_point = "./tmp/cifs" 
    run("rm -rdf {mount_point}")
    os.makedirs(mount_point, exist_ok=True)
    assert is_empty(mount_point), "Mount point should be empty before test"

    with cifs(qdrive_ip, q_drive_path, mount_point, svn_user, svn_pass):
        # Perform your tests here
        # has at lest some folder or files under mount point
        assert not is_empty(mount_point), "Mount point should not be empty"

    assert is_empty(mount_point), "Mount point should be empty after unmounting"


def test_sshfs_mount():
    mount_point = "./tmp/cifs" 
    run("rm -rdf {mount_point}")
    os.makedirs(mount_point, exist_ok=True)
    assert is_empty(mount_point), "Mount point should be empty before test"

    with sshfs("qlfs04", "/home/qp/", mount_point, "qp", "qlabs4ever"):
        # Perform your tests here
        # has at lest some folder or files under mount point
        assert not is_empty(mount_point), "Mount point should not be empty"

    assert is_empty(mount_point), "Mount point should be empty after unmounting"