#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import json
import smtplib

from email.message import EmailMessage
from json import JSONDecodeError

from config import Config
from logger import Logger


class Mailer(object):
    __instance: 'Mailer' = None

    @staticmethod
    def send(content="Hello World!") -> None:  # TODO
        if Mailer.__instance is None:
            Mailer()

        if Mailer.__instance.init_ok:
            # TODO
            print('YAY')
            return
            smtp = smtplib.SMTP(Mailer.__instance.smtp_host, Mailer.__instance.smtp_port)
            Mailer.__instance.msg.set_content(content)
            smtp.send_message(Mailer.__instance.msg)
            smtp.quit()

    def __init__(self) -> None:
        if Mailer.__instance is not None:
            raise Exception("This class is a singleton!")

        Mailer.__instance = self

        self.init_ok: bool = False
        self.msg: EmailMessage = None
        self.smtp_host: str = Config.get('MAILER', 'smtp_host')
        self.smtp_port: str = Config.get('MAILER', 'smtp_port')

        _subject = Config.get('MAILER', 'Subject')
        _sender = Config.get('MAILER', 'sender')
        try:
            _receivers = json.loads(Config.get('MAILER', 'receivers'))
        except JSONDecodeError:
            Logger.get().warn('Problems decoding email receivers!')
            _receivers = None

        if not _subject or not _sender or not _receivers or not self.smtp_host or not self.smtp_port:
            Logger.get().warn('Emails not being sent!')
            return

        self.msg = EmailMessage()
        self.msg.set_charset('utf-8')
        self.msg['Subject'] = Config.get('MAILER', 'Subject')
        self.msg['From'] = Config.get('MAILER', 'sender')
        self.msg['To'] = json.loads(Config.get('MAILER', 'receivers'))

        self.init_ok = True
