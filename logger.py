#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import logging
from logging.handlers import RotatingFileHandler

from config import Config


class Logger(object):
    __instance = None

    @staticmethod
    def get():
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self) -> None:
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")

        log_handler = RotatingFileHandler(Config.get('LOGGER', 'log_file', '/dev/null'), mode='a',
                                          maxBytes=5 * 1024 * 1024, backupCount=2, encoding=None, delay=0)
        log_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        log_handler.setLevel(logging.INFO)

        Logger.__instance = logging.getLogger('root')
        Logger.__instance.setLevel(logging.INFO)
        Logger.__instance.addHandler(log_handler)
