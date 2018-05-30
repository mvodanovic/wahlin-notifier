#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import logging
from logging.handlers import RotatingFileHandler

from app.config import Config


class Logger(object):
    __instance = {}

    @staticmethod
    def get(name: str):
        if name not in Logger.__instance:
            Logger(name)
        return Logger.__instance[name]

    def __init__(self, name: str) -> None:
        if name in Logger.__instance:
            raise Exception("Logger '{}' already exists!".format(name))

        log_handler = RotatingFileHandler(Config.get('LOGGER', 'log_file', '/dev/null'), mode='a',
                                          maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None, delay=0)
        log_handler.setFormatter(logging.Formatter('%(asctime)s <%(name)s> [%(levelname)s] %(message)s'))
        log_handler.setLevel(logging.INFO)

        Logger.__instance[name] = logging.getLogger(name)
        Logger.__instance[name].setLevel(logging.INFO)
        Logger.__instance[name].addHandler(log_handler)
