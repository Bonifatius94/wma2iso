
# WMA CD Writer

## About
This project creates auto-play CD ROM disks to play WMA music files.

## Prerequisites

1) Install Python 3, see the [official download site](https://www.python.org/downloads/)

2) Install the PIP packages

```sh
python3 -m pip install -r requirements.txt
```

## Usage

1) Put the WMA files to be burned into one folder (subdirectories are supported).

2) Execute following commands to create a burnable ISO file:

```sh
python3 wma2iso.py wma_files mydisk.iso
```

## Depedencies
This project depends on pycdlib for creating ISO files.
Special thanks for providing the very easy-to-use genisoimage script.
