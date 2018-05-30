#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import errno
import os

import requests

from logger import Logger
from mailer import Mailer


CACHE_FILE = '.cache.html'
# FETCH_URL = 'http://foo.bar'
FETCH_URL = 'http://wahlinfastigheter.se/lediga-objekt/lagenhet/'
BROWSER_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
START_TAG = '<!-- Start lediga lägenheter -->'
END_TAG = '<!-- Slut lediga lägenheter -->'
NO_CONTENT = 'Just nu har vi tyvärr inga lediga lägenheter att förmedla här.'

# noinspection PyBroadException
try:
    response = requests.get(FETCH_URL, headers=BROWSER_HEADERS)
except Exception as e:
    Logger.get().error(str(e))
    exit(1)

# noinspection PyUnboundLocalVariable
if response.status_code >= 300:
    Logger.get().error('{}: {}'.format(response.status_code, response.content))
    exit(1)

contents = response.content.decode('utf-8')

contents = contents[contents.index(START_TAG) + len(START_TAG):contents.index(END_TAG)].strip()

if contents.index(NO_CONTENT) >= 0:
    Logger.get().info("No new contents.")
    try:
        os.remove(CACHE_FILE)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
    exit(0)

f = open(CACHE_FILE, 'r+')

if f.read() == contents:
    Logger.get().info("No new contents.")
    exit(0)

Logger.get().info("New content detected.")
f.truncate()
f.write(contents)
Mailer.send()

print(contents)
