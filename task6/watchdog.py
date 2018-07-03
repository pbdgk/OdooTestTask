import os
import time
import glob
import json

from models.file_handlers import FileHandler


def load_config(config_name):
    try:
        with open(config_name) as f:
            return json.load(f)
    except FileNotFoundError:
        print('Config does not exist here -> %s' % os.path.abspath(config_name))
        exit()
    except json.JSONDecodeError as e:
        print('Can\'t parse config. Fix erros', e, sep='\n')
        exit()


class Watchdog:

    def __init__(self, config):
        self.file_handler = FileHandler(config)
        self._glob_pattern = '*'
        protected_files = config.get('protected', [])
        self.__protected_files = {__file__, *protected_files}

    @property
    def glob_pattern(self):
        return self._glob_pattern

    @glob_pattern.setter
    def glob_pattern(self, path_pattern):
        if not isinstance(path_pattern, str):
            raise ValueError('Path pattern must be "str" type')
        if os.path.isabs(path_pattern):
            raise ValueError('Absolute path patterns are restricted!')
        self._glob_pattern = path_pattern

    def watch(self):
        print('Watching ...')
        while True:
            files = set(glob.glob(self._glob_pattern))
            files = files - self.__protected_files
            if files:
                self.file_handler.manage(files)
            time.sleep(.8)


if __name__ == '__main__':
    config = load_config('config.json')
    Watchdog(config).watch()
