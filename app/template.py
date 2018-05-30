#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from typing import Dict


class MailTemplate(object):
    def __init__(self, url: str, links: Dict[str, str]) -> None:
        self.url: str = url
        self.links: Dict[str, str] = links
        self.template: str = None

    def get(self) -> str:
        if self.template is None:
            prefix = "\n    *"
            parsed_links = prefix + prefix.join("{}: {}".format(name, url) for (url, name) in self.links.items())
            self.template = "{}:\n{}".format(self.url, parsed_links)
        print(self.template)
        exit(0)
        return self.template
