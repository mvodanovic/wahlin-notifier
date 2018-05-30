#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from app.mailer import Mailer
from app.parser import Parser
from app.template import MailTemplate
from app.url_fetcher import URLFetcher


fetcher = URLFetcher()
fetcher.fetch()

if fetcher.content:
    parser = Parser(fetcher.content)
    parser.parse()

    if parser.has_new_content:
        Mailer.send(MailTemplate(fetcher.url, parser.links))
