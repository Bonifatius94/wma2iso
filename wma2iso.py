import os
import sys
import shutil
from glob import glob
from typing import List, Tuple


PYTHON_EXE='python3'


def create_iso(
        wma_source_dir: str,
        iso_outfile: str,
        iso_temp_dir: str='iso_temp'):

    if os.path.exists(iso_temp_dir) and os.path.isdir(iso_temp_dir):
        print(f"ISO directory '{iso_temp_dir}' is not empty, will be wiped and recreated.")
        shutil.rmtree(iso_temp_dir, ignore_errors=False, onerror=None)

    print('prepare files to be written to the ISO')
    shutil.copytree(wma_source_dir, iso_temp_dir)

    print("create 'AutoList.wpl' and 'AUTORUN.INF' files")
    wma_files = files_of_pattern_inside_folder(iso_temp_dir, './**/*.wma')
    create_autolist_wpl_file(wma_files, iso_temp_dir)
    create_autorun_file(iso_temp_dir)

    print("generate ISO file '{iso_outfile}'")
    isogen_py = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pycdlib-genisoimage.py')
    os.system(f'{PYTHON_EXE} {isogen_py} -o {iso_outfile} -R -J -D {iso_temp_dir}')
    # TODO: figure out if the flags -R -J -D are required to make auto-play work
    shutil.rmtree(iso_temp_dir)


def create_autolist_wpl_file(
        music_files: List[str],
        iso_dir: str,
        wpl_file: str='AutoList.wpl'):
    media_tags = [f'<media src="{music_path}"/>' for music_path in music_files]
    wpl_content = f'<smil><body><seq>{" ".join(media_tags)}</seq></body></smil>'

    wpl_filepath = os.path.join(iso_dir, wpl_file)
    with open(wpl_filepath, mode='w', encoding='utf-8') as file:
        file.write(wpl_content)


def create_autorun_file(iso_dir: str, autorun_file: str='AUTORUN.INF'):
    autorun_filepath = os.path.join(iso_dir, autorun_file)
    with open(autorun_filepath, mode='w', encoding='ascii') as file:
        file.write('[autorun]\nshellexecute=AutoList.wpl')


def read_script_args() -> Tuple[str, str, str]:
    if len(sys.argv) < 3:
        print('Insufficient arguments! This script expects the WMA source directory '
              'as first and the ISO output file as second argument!')
        exit(1)

    wma_source_dir = sys.argv[1]
    iso_outfile = sys.argv[2]

    if not os.path.exists(wma_source_dir) or not os.path.isdir(wma_source_dir):
        print(f"Invalid argument! WMA source directory '{wma_source_dir}' does not exist!")
        exit(1)

    if not iso_outfile.endswith('.iso'):
        print(f"Invalid argument! Output ISO file '{iso_outfile}' has wrong file extension (expected *.iso)!")
        exit(1)

    if len(files_of_pattern_inside_folder(wma_source_dir, './**/*.wma')) == 0:
        print(f"No WMA files found in source directory '{wma_source_dir}'!")
        exit(1)

    return wma_source_dir, iso_outfile, 'iso_temp'


def files_of_pattern_inside_folder(folder: str, pattern: str) -> List[str]:
    working_dir = os.getcwd()
    os.chdir(folder)
    files = glob(pattern, recursive=True)
    os.chdir(working_dir)
    return files


def main():
    wma_source_dir, iso_outfile, iso_temp_dir = read_script_args()
    create_iso(wma_source_dir, iso_outfile, iso_temp_dir)
    # TODO: try to figure out how to burn an ISO file to a CD-ROM


if __name__ == '__main__':
    main()
