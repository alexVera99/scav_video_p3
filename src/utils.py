"""Utils functions to solve common problems in all the exercises."""

import pathlib
import subprocess
import logging

SHELL_ERRORS = ["error",
                "failed",
                "invalid",
                "no such file or directory"]


def exec_in_shell_wrapper(cmd: list) -> tuple:
    """
    Execute command in Linux shell.

    :param cmd: command to execute. Type: list
    :return: a tuple with the stdout and stderr
    """
    with subprocess.Popen(cmd,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as run_cmd:

        stdout, stderr = run_cmd.communicate()

    return stdout, stderr


def check_shell_stderr(stderr,
                       logging_output: str = "Something went wrong"):
    """
    Check the output of the stderr of a shell command.\
    If error is found, it throws an exception\
    along with the output of the stderr.

    :param stderr: stderr output from a shell command
    :param logging_output: any message to be shown in the exception if any\
    error is found.
    :return: no return
    """
    # Convert to str
    stderr = stderr.decode('ascii')

    for _e in SHELL_ERRORS:
        if _e not in stderr.lower():
            continue
        logging.error(logging_output + "\n" + stderr)
        raise Exception(logging_output)


def rename_from_path(filename_path: pathlib.Path,
                     new_filename: str,
                     new_extension: str = None) -> pathlib.Path:
    """
    Rename file name.

    :param filename_path: file name with its path
    :param new_filename: new file name use to change the previous one
    :param new_extension: new file name extension to change the previous one
    :return: new filename with the correct extension and path
    """
    parent_path = filename_path.parent.resolve()

    if new_extension is None:
        new_extension = filename_path.name.split(".")[1]

    return parent_path / f"{new_filename}.{new_extension}"
