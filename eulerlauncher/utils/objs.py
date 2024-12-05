import os
import configparser

from eulerlauncher.utils import exceptions


class Conf(object):

    def __init__(self, config_file) -> None:
        self.conf = configparser.ConfigParser()
        if not os.path.exists(config_file):
            raise exceptions.NoSuchFile(file=config_file)
        self.conf.read(config_file)
