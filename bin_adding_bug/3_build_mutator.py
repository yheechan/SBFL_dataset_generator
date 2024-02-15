#!/usr/bin/python3
import subprocess as sp
from pathlib import Path
import os
import argparse

script_file_path = Path(os.path.realpath(__file__))
bin_dir = script_file_path.parent

if __name__ == "__main__":
    music_dir = bin_dir / 'MUSIC'
    if not music_dir.exists():
        cmd = [
            'git', 'clone', 'https://github.com/swtv-kaist/MUSIC.git'
        ]
        sp.call(cmd, cwd=bin_dir)
    else:
        print('MUSIC already exists')
    
    music_exe = music_dir / 'music'
    if not music_exe.exists():
        cmd = ['make', '-j20']
        res = sp.call(cmd, cwd=music_dir)
        print('MUSIC build: {}'.format(res))
    else:
        print('MUSIC already built')
