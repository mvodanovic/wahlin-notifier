#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import configparser
import json
from typing import Any


class Config(object):
    CONFIG_FILE = 'conf/wahlin.ini'

    __instance: 'Config' = None

    @staticmethod
    def get(section: str, option: str, default_value: str = None, param_type: str = "str") -> Any:
        if Config.__instance is None:
            Config()

        if section not in Config.__instance.config:
            value = default_value

        elif option not in Config.__instance.config[section]:
            value = default_value

        else:
            value = Config.__instance.config[section][option]

        if param_type == "str":
            return value
        elif param_type == "json":
            return json.loads(value) if value is not None else None
        else:
            raise Exception("Unsupported param type!")

    def __init__(self) -> None:
        if Config.__instance is not None:
            raise Exception("This class is a singleton!")

        self.config: configparser.ConfigParser = configparser.ConfigParser()

        self.config.read(Config.CONFIG_FILE)

        Config.__instance = self
