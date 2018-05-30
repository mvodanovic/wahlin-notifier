#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8


import errno
import os
from typing import Dict

from bs4 import BeautifulSoup

from app.config import Config
from app.logger import Logger


class Parser(object):
    def __init__(self, html: str) -> None:
        self.html: str = html
        self.has_new_content: bool = False
        self.links: Dict[str, str] = {}

    def parse(self) -> None:
        contents = self.html[self.html.index(Config.get('PARSER', 'start_tag')) + len(
            Config.get('PARSER', 'start_tag')):self.html.index(Config.get('PARSER', 'end_tag'))].strip()

        if Config.get('PARSER', 'empty_pattern') in contents:
            Logger.get(self.__class__.__name__).info("No new contents.")
            self.has_new_content = False
            self.links = {}
            try:
                os.remove("{}/{}".format(Config.get('CRON', 'project_root'), Config.get('PARSER', 'cache_file')))
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
            return

        with open(Config.get('PARSER', 'cache_file'), 'a+') as f:
            f.seek(0)
            if f.read() == contents:
                Logger.get(self.__class__.__name__).info("No new contents.")
                self.has_new_content = False
                self.links = {}
            else:
                Logger.get(self.__class__.__name__).info("New content detected.")
                self.has_new_content = True
                self._extract_links(contents)
                f.seek(0)
                f.truncate()
                f.write(contents)

    def _extract_links(self, contents: str) -> None:
        soup = BeautifulSoup(contents, 'html.parser')
        self.links = {link.get('href'): link.get('title') for link in soup.find_all('a') if
                      link.get('title') is not None}
