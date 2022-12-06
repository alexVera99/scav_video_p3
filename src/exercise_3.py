"""Solution for Exercise 3. This has been inspired by \
http://tinsy.me/y8nifw"""
import logging
import pathlib
from concurrent.futures import ProcessPoolExecutor
import utils as ut


def start_livestreaming(filename_path: pathlib.Path,
                        ip_address):
    """
    Start a livestreaming of the given video.

    :param filename_path: video filename path to live stream
    :param ip_address: ip_address address to transmit the video
    :return: no return
    """

    if not filename_path.exists():
        print("Not found")
        logging.exception(FileNotFoundError(f"File not found {filename_path}"))

    cmd = ["ffmpeg", "-i", filename_path,
           "-v", "0", "-vcodec", "mpeg4",
           "-f", "mpegts", ip_address]

    logging.info("Starting the live stream for %s...", filename_path)

    _, stderr = ut.exec_in_shell_wrapper(cmd)
    ut.check_shell_stderr(stderr)

def consume_livestreaming(ip_address):
    """
    Consume streaming in the given ip_address a live streaming of the given video.

    :param ip_address: ip_address where the streaming is happening
    :return: no return
    """
    title = f"Consuming livestream from {ip_address}"
    cmd = ["ffplay", "-alwaysontop",
           "-window_title", title,
           ip_address]

    logging.info("Listening the live stream in %s...", ip_address)

    _, stderr = ut.exec_in_shell_wrapper(cmd)
    ut.check_shell_stderr(stderr)


def main():
    """
    Test the above functions.

    :return no return
    """
    video_filename = pathlib.Path("../data/bbb.mp4")
    ip_address = "udp://127.0.0.1:23000"

    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.submit(start_livestreaming,
                        video_filename,
                        ip_address)

        executor.submit(consume_livestreaming,
                        ip_address)


if __name__ == "__main__":
    main()
