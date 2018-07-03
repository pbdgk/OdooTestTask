import os
import shutil
import glob
import json
import time


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


class FileHandler:
    """
        # TODO:
            - remember files by saving checksum of file
            - add file size limit

    """
    def __init__(self, config):
        self.config = config
        self.processed_files = set()

    def manage(self, files):
        for filename in files:
            if self.is_file(filename):
                self.do_action(filename)

    def do_action(self, filename):
        extension = self.get_extension(filename)
        if extension in self.config["copy"]["extensions"]:
            self.copy(filename)

        elif extension in self.config["remove"]["extensions"]:
            self.remove(filename)

        elif extension in self.config["rename"]["extensions"]:
            self.remove(filename)

    def copy(self, filename):
        if filename not in self.processed_files:
            destination_dir = self.config["copy"]["destinationDir"]
            destination = os.path.join(destination_dir, filename)
            result = self.copy_file(filename, destination)
            self.processed_files.add(filename)
            print(result)

    def rename(self, filename):
        result = self.rename_file(filename)
        print(result)

    def remove(self, filename):
        rename_to = filename + self.config["rename"]["renameTo"]
        result = self.remove_file(filename)
        print(result)

    @staticmethod
    def copy_file(filename, destination):
        try:
            # TODO: check if file with same name exist
            new_path = shutil.copy(filename, destination)
            message = os.path.abspath(new_path)
        except (NotADirectoryError, FileNotFoundError) as e:
            print("""
                Destination folder does not exist. Create it manualy
                or fix "destinationDir" in config.
                """)
            exit()

        return message

    @staticmethod
    def rename_file(filename, new_filename):
        try:
            os.rename(filename, new_filename)
            message = 'Renamed %s to %s' % (filename, new_filename)
        except FileNotFoundError:
            message = 'Seems somebody remove/rename file allready, so it is not \
                       reachable by name: %s' % filename
        return message

    @staticmethod
    def remove_file(filename):
        try:
            os.remove(filename)
            message = 'Removed file %s' % filename
        except (FileNotFoundError, PermissionError) as e:
            message = e
        return message

    @staticmethod
    def is_file(filename):
        return os.path.isfile(filename)

    @staticmethod
    def get_extension(filename):
        return os.path.splitext(filename)[1]


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
            print('Current state: %s' % files)
            if files:
                self.file_handler.manage(files)
            time.sleep(.8)


if __name__ == '__main__':
    config = load_config('config.json')
    Wathdog(config).watch()
