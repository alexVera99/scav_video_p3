"""Solution for Exercise 1."""
import logging
import pathlib
import json
import src.utils as ut


def build_hls_container(filename_path: pathlib.Path,
                        output_dir_path: pathlib = pathlib.Path("")
                        ) -> pathlib.Path:
    """
    Builds an HLS container of the given video. Inspired in \
    https://ottverse.com/hls-packaging-using-ffmpeg-live-vod.

    :param filename_path: video filename path
    :param output_dir_path: (optional) output directory path
    :return: path of the hls container
    """

    if output_dir_path == pathlib.Path(""):
        dir_name = filename_path.name.split(".")[0]
        dir_path = filename_path.parent
        output_dir_path = dir_path / f"{dir_name}_HLS"

    cmd = ['ffmpeg', '-y', '-i', filename_path,
           '-filter_complex', '[0:v]split=3[v1][v2][v3];'
           '[v1]copy[v1out];' '[v2]scale=w=1280:h=720[v2out];'
           '[v3]scale=w=640:h=360[v3out]', '-map', '[v1out]', '-c:v:0',
           'libx264', '-x264-params', 'nal-hrd=cbr:force-cfr=1', '-b:v:0',
           '5M', '-maxrate:v:0', '5M', '-minrate:v:0', '5M', '-bufsize:v:0',
           '10M', '-preset', 'slow', '-g', '48', '-sc_threshold', '0',
           '-keyint_min', '48', '-map', '[v2out]', '-c:v:1', 'libx264',
           '-x264-params', 'nal-hrd=cbr:force-cfr=1', '-b:v:1', '3M',
           '-maxrate:v:1', '3M', '-minrate:v:1', '3M', '-bufsize:v:1', '3M',
           '-preset', 'slow', '-g', '48', '-sc_threshold', '0',
           '-keyint_min', '48', '-map', '[v3out]', '-c:v:2', 'libx264',
           '-x264-params', 'nal-hrd=cbr:force-cfr=1', '-b:v:2', '1M',
           '-maxrate:v:2', '1M', '-minrate:v:2', '1M', '-bufsize:v:2', '1M',
           '-preset', 'slow', '-g', '48', '-sc_threshold', '0',
           '-keyint_min', '48', '-map', 'a:0', '-c:a:0', 'aac', '-b:a:0',
           '96k', '-ac', '2', '-map', 'a:0', '-c:a:1', 'aac', '-b:a:1',
           '96k', '-ac', '2', '-map', 'a:0', '-c:a:2', 'aac', '-b:a:2',
           '48k', '-ac', '2', '-f', 'hls', '-hls_time', '2',
           '-hls_playlist_type', 'vod', '-hls_flags', 'independent_segments',
           '-hls_segment_type', 'mpegts', '-hls_segment_filename',
           output_dir_path / 'stream_%v/data%02d.ts', '-master_pl_name',
           output_dir_path / 'master.m3u8',
           '-var_stream_map', 'v:0,a:0 v:1,a:1 v:2,a:2',
           output_dir_path / 'stream_%v.m3u8']

    logging.info(f"Building the HLS container for {filename_path}...")

    _, stderr = ut.exec_in_shell_wrapper(cmd)
    ut.check_shell_stderr(stderr)

    logging.info(f"HLS container for {filename_path}")

    return output_dir_path


def main():
    """
    Test the above functions.

    :return no return
    """
    video_filename = pathlib.Path("../data/bbb.mp4")

    hls_container_dir = build_hls_container(video_filename)

    print(hls_container_dir)


if __name__ == "__main__":
    main()
