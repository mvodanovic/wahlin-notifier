#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from json import JSONDecodeError
from typing import Optional

import requests

from app.config import Config
from app.logger import Logger


class URLFetcher(object):
    def __init__(self) -> None:
        self.url = Config.get('URL_FETCHER', 'url')
        try:
            self.headers = Config.get('URL_FETCHER', 'headers', param_type="json")
        except JSONDecodeError:
            Logger.get(self.__class__.__name__).warn("Problem decoding URL headers from JSON in config!")
            self.headers = None
        self.content: Optional[str] = None

    def fetch(self) -> None:
        # noinspection PyBroadException
        try:
            response = requests.get(self.url, headers=self.headers)
        except Exception as e:
            Logger.get(self.__class__.__name__).error(str(e))
            self.content = None
            return

        if response.status_code >= 300:
            Logger.get(self.__class__.__name__).error('{}: {}'.format(response.status_code, response.reason))
            self.content = None
        else:
            self.content = response.content.decode('utf-8')
