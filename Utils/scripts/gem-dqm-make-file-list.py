#!/usr/bin/env python3
r"""
TODO
- [ ] how about making a dict like storage.xml in the SITECONF
"""
from pathlib import Path
import socket
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', type=Path)
    parser.add_argument('-p', '--pathname', type=str, default='*.root')
    parser.add_argument('-o', '--output-path', type=str)
    args = parser.parse_args()

    if not args.input_dir.is_dir():
        raise IsADirectoryError(args.input_dir)

    if args.output_path is None:
        args.output_path = Path.cwd().joinpath(f'filelist-{args.input_dir.name}').with_suffix('.txt')
    if args.output_path.exists():
        raise FileExistsError(args.output_path)

    file_list = args.input_dir.glob(args.pathname)
    file_list = [str(each.resolve()) for each in file_list]

    hostname = socket.gethostname()
    if hostname in ('ui10.sdfarm.kr', 'ui20.sdfarm.kr'):
        if str(args.input_dir).startswith('/xrootd/'):
            file_list = [each.replace('/xrootd/', 'root://cms-xrdr.private.lo:2094//xrd/') for each in file_list]
        else:
            raise NotImplementedError(f'hostname={hostname} but input_dir={args.input_dir}')
    elif hostname in ('gate', ):
        file_list = ['file:' + each for each in file_list]
    else:
        raise NotImplementedError(hostname)

    text = '\n'.join(file_list)
    with open(args.output_path, 'w') as txt_file:
        txt_file.write(text)


if __name__ == '__main__':
    main()
