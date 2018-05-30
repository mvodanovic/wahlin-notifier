#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from typing import List


class MailTemplate(object):
    def __init__(self, url: str, links: List[str]) -> None:
        self.url: str = url
        self.links: List[str] = links
        self.template: str = None

    def get(self) -> str:
        if self.template is None:
            list_prefix = "\n    *"
            parsed_links = list_prefix + list_prefix.join(self.links)
            self.template = "{}\n{}".format(self.url, parsed_links)
        return self.template
