#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from abc import ABC, abstractmethod
from typing import Dict


class AbstractMailTemplate(ABC):
    @abstractmethod
    def get(self):
        pass


class MailTemplate(AbstractMailTemplate):
    def __init__(self, url: str, links: Dict[str, str]) -> None:
        self.url: str = url
        self.links: Dict[str, str] = links
        self.template: str = None

    def get(self) -> str:
        if self.template is None:
            prefix = "\n    *"
            parsed_links = prefix + prefix.join("{}: {}".format(name, url) for (url, name) in self.links.items())
            self.template = "{}:\n{}".format(self.url, parsed_links)
        return self.template


class TestMailTemplate(AbstractMailTemplate):
    def __init__(self):
        pass

    def get(self) -> str:
        return "This is a test email"
