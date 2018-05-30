#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8


import errno
import os
from typing import List

from app.config import Config
from app.logger import Logger


class Parser(object):
    def __init__(self, html: str) -> None:
        self.html: str = html
        self.has_new_content: bool = False
        self.links: List[str] = []

    def parse(self) -> None:
        contents = self.html[self.html.index(Config.get('PARSER', 'start_tag')) + len(
            Config.get('PARSER', 'start_tag')):self.html.index(Config.get('PARSER', 'end_tag'))].strip()

        if contents.index(Config.get('PARSER', 'empty_pattern')) >= 0:
            Logger.get(self.__class__.__name__).info("No new contents.")
            self.has_new_content = False
            self.links = []
            try:
                os.remove(Config.get('PARSER', 'cache_file'))
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
            return

        f = open(Config.get('PARSER', 'cache_file'), 'r+')

        if f.read() == contents:
            Logger.get(self.__class__.__name__).info("No new contents.")
            self.has_new_content = False
            self.links = []
        else:
            Logger.get(self.__class__.__name__).info("New content detected.")
            self.has_new_content = True
            # TODO: links
            f.truncate()
            f.write(contents)
