import json
import os

from common import *

class FileOps:
    def __init__(self, file_dir, file_name):
        self.file_path = os.path.join(file_dir, file_name)
        self.host_list = []

    def backup_file(self):
        with open(self.file_path, "r") as f:
            with open(self.file_path + ".bak", "w") as bak:
                bak.write(f.read())

    def get_json_data(self):
        with open(self.file_path) as f:
            return json.load(f)
        pass

    def update_cfg_file(self, cfg: dict):
        if cfg is None:
            cfg = DEFAULT_CFG
        try:
            with open(self.file_path, "w") as f:
                f.write(json.dumps(cfg, indent=4))
        except:
            with open(self.file_path, "w") as f:
                f.write(json.dumps(DEFAULT_CFG, indent=4))
