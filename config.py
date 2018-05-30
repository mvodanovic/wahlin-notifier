#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import configparser


class Config(object):
    CONFIG_FILE = 'wahlin.ini'

    __instance: 'Config' = None

    @staticmethod
    def get(section, option, default_value=None):
        if Config.__instance is None:
            Config()

        if section not in Config.__instance.config:
            return default_value

        if option not in Config.__instance.config[section]:
            return default_value

        return Config.__instance.config[section][option]

    def __init__(self) -> None:
        if Config.__instance is not None:
            raise Exception("This class is a singleton!")

        self.config: configparser.ConfigParser = configparser.ConfigParser()

        self.config.read(Config.CONFIG_FILE)

        Config.__instance = self
