from enum import Enum
from pathlib import Path

from scanfs.volumes import volumes


class File:
    def __init__(self, file_path: Path):
        self._path = file_path

    def size(self):
        print(f"{self._path}: {self._path.stat().st_size}")
        return self._path.stat().st_size

    def get_block_device(self):
        """Returns block device file is stored on

        Returns:
            _type_: _description_
        """
        return volumes.get_by_raw_device_number(self._path.stat().st_dev)


class RegularFile(File):
    pass


class Directory(File):
    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self._children = []
        for child in self._path.iterdir():
            self._children.append(process_file(child))

    def size(self):
        total_size = self._path.stat().st_size
        if self._children:
            total_size += sum(map(lambda x: x.size(), self._children))
        print(f"{self._path}: {total_size}")
        return total_size


class SpecialFile(File):
    """Class for special files that are not regular files or directories

    Supported types:
      * Block devices
      * Character devices
      * Pipes (FIFO)
      * Symlinks
      * Sockets

    If the file type is not a regular file, diectory,
    or any of the types above it will be marked as unknown.
    """

    class SpecialFileType(Enum):
        BLOCK = "b"
        CHAR = "c"
        PIPE = "p"
        SYMLINK = "l"
        SOCKET = "s"
        UNKNOWN = "u"

    def special_type(self):
        if self._path.is_symlink():
            return self.SpecialFileType.SYMLINK
        elif self._path.is_socket():
            return self.SpecialFileType.SOCKET
        elif self._path.is_block_device():
            return self.SpecialFileType.BLOCK
        elif self._path.is_char_device():
            return self.SpecialFileType.CHAR
        elif self._path.is_fifo():
            return self.SpecialFileType.PIPE
        else:
            return self.SpecialFileType.UNKNOWN


def process_file(file_path: Path):
    if file_path.is_file() and not file_path.is_symlink():
        return RegularFile(file_path)
    elif file_path.is_dir() and not file_path.is_symlink():
        return Directory(file_path)
    else:
        return SpecialFile(file_path)
