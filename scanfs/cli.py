from pathlib import Path

from scanfs.file import Directory, SpecialFile, RegularFile
from scanfs.file import process_file


def scan(base_path: Path):
    root_dir = Directory(Path("/"))
