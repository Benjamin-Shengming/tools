import os
from contextlib import contextmanager
from loguru import logger
from qutil.shell.local import run as run_command

def fuserumount(mount_point): 
    """
    Unmount mount_point using fusermount.
    """
    command = f"fusermount -u {mount_point}"
    run_command(command)

def umount(mount_point):
    """
    Unmount mount_point.
    """
    command = f"sudo umount -lf {mount_point}"
    run_command(command)

def cifs_mount(cifs_ip, cifs_path, mount_point, user, password):
    """
    Mount a CIFS share.
    """
    os.makedirs(mount_point, exist_ok=True)
    cifs_full_path = f"//{cifs_ip}/{cifs_path.strip('/')}"
    command = f"sudo mount -t cifs {cifs_full_path} {mount_point} -o ro,username={user},password={password},vers=2.1"
    return run_command(command)

def sshfs_mount(ssh_ip, ssh_path, mount_point, user, password):
    """
    Mount a remote directory over SSHFS.
    """
    os.makedirs(mount_point, exist_ok=True)
    command = f"echo {password} | sshfs -o password_stdin -o StrictHostKeyChecking=no {user}@{ssh_ip}:{ssh_path} {mount_point} "
    return run_command(command, pty=False)

# Context manager to temporarily set environment variables
@contextmanager
def sshfs(ssh_ip, ssh_path, mount_point, user, password):
    """
    Temporarily set environment variables for SSHFS mount.
    """
    exit_code = 1 
    try:
        ret = sshfs_mount(ssh_ip, ssh_path, mount_point, user, password)
        exit_code = ret["exit_code"]
        yield
    finally:
        if exit_code == 0:
            fuserumount(mount_point)


@contextmanager 
def cifs(cifs_ip, cifs_path, mount_point, user, password):
    """
    Temporarily set environment variables for CIFS mount.
    """
    try:
        cifs_mount(cifs_ip, cifs_path, mount_point, user, password)
        yield
    finally:
        umount(mount_point)
