import os
import shutil


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
                try:
                    self.do_action(filename)
                except KeyError:
                    print('Key Error. Seems that config has errors')

    def do_action(self, filename):
        extension = self.get_extension(filename)
        if extension in self.config["copy"]["extensions"]:
            message = self.copy(filename)

        elif extension in self.config["remove"]["extensions"]:
            message = self.remove(filename)

        elif extension in self.config["rename"]["extensions"]:
            message = self.rename(filename)

    def copy(self, filename):
        if filename not in self.processed_files:
            destination_dir = self.config["copy"]["destinationDir"]
            copy_filename = self.config["copy"]["prefix"] + filename
            destination = os.path.join(destination_dir, copy_filename)
            result = self.copy_file(filename, destination)
            self.processed_files.update({filename, copy_filename})
            print(result)

    def remove(self, filename):
        result = self.remove_file(filename)
        print(result)

    def rename(self, filename):
        rename_to = filename + self.config["rename"]["renameTo"]
        result = self.rename_file(filename, rename_to)
        print(result)

    @staticmethod
    def copy_file(filename, destination):
        try:
            # TODO: check if file with same name exist
            new_path = shutil.copy(filename, destination)
        except (NotADirectoryError, FileNotFoundError) as e:
            print("""
                Destination folder does not exist. Create it manualy
                or fix "destinationDir" in config.
                """)
            exit()

        message = os.path.abspath(new_path)
        return message

    @staticmethod
    def rename_file(filename, new_filename):
        try:
            os.rename(filename, new_filename)
            message = 'Renamed %s to %s' % (filename, new_filename)
        except FileNotFoundError:
            message = 'Seems somebody remove/rename file allready, so it is not\
                       reachable by name: %s' % filename
        except PermissionError:
            message = 'Permission denied. This folder protected with admin rights'
        return message

    @staticmethod
    def remove_file(filename):
        try:
            os.remove(filename)
            message = 'Removed file %s' % filename
        except FileNotFoundError:
            message = 'Seems somebody remove/rename file allready, so it is not\
                       reachable by name: %s' % filename
        except PermissionError:
            message = 'Permission denied. This folder protected with admin rights'
        return message

    @staticmethod
    def is_file(filename):
        return os.path.isfile(filename)

    @staticmethod
    def get_extension(filename):
        return os.path.splitext(filename)[1]
