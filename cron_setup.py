#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import subprocess

from app.config import Config

commands = [
    'cd {}'.format(Config.get('CRON', 'project_root')),
    '. venv/bin/activate',
    './run.py'
]

logging = '&>{}/{}'.format(Config.get('CRON', 'project_root'), Config.get('CRON', 'log_file'))

cron_cmd = '(crontab -l 2>/dev/null ; echo "{} {} {}") | sort - | uniq - | crontab -'.format(
    Config.get('CRON', 'schedule'), " && ".join(commands), logging)

subprocess.call(cron_cmd, shell=True)
