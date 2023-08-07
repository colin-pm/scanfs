import json
import os
import subprocess


class Volumes:
    def __init__(self):
        ret = subprocess.run(["lsblk", "--json"], capture_output=True, check=True)
        self.block_devices = json.loads(ret.stdout)["blockdevices"]
        self._lookup_table = {}
        self._create_lookup_table()

    def get_by_major_minor(self, major: int, minor: int):
        return self._lookup_table[f"{major}:{minor}"]

    def get_by_raw_device_number(self, rdm: int):
        return self.get_by_major_minor(os.major(rdm), os.minor(rdm))

    def _create_lookup_table(self):
        for block_device in self.block_devices:
            self._rec_search_block_device(block_device)

    def _rec_search_block_device(self, device):
        maj_min = device["maj:min"]
        self._lookup_table[maj_min] = device
        if "children" in device:
            for child in device["children"]:
                self._rec_search_block_device(child)


volumes = Volumes()
