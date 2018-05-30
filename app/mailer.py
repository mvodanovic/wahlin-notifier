#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import smtplib
from email.message import EmailMessage
from json import JSONDecodeError

from app.config import Config
from app.logger import Logger
from app.template import MailTemplate


class Mailer(object):
    __instance: 'Mailer' = None

    @classmethod
    def send(cls, content: MailTemplate) -> None:
        if Mailer.__instance is None:
            Mailer()

        if Mailer.__instance.init_ok:
            smtp = smtplib.SMTP_SSL("{}:{}".format(Mailer.__instance.smtp_host, Mailer.__instance.smtp_port))
            try:
                smtp.login(Mailer.__instance.smtp_user, Mailer.__instance.smtp_password)
            except smtplib.SMTPAuthenticationError as e:
                Logger.get(cls.__name__).warn(str(e))
                return
            Mailer.__instance.msg.set_content(content.get())
            try:
                smtp.send_message(Mailer.__instance.msg)
            except smtplib.SMTPDataError as e:
                Logger.get(cls.__name__).warn(str(e))
            smtp.quit()

    def __init__(self) -> None:
        if Mailer.__instance is not None:
            raise Exception("This class is a singleton!")

        Mailer.__instance = self

        self.init_ok: bool = False
        self.msg: EmailMessage = None
        self.smtp_host: str = Config.get('MAILER', 'smtp_host')
        self.smtp_port: str = Config.get('MAILER', 'smtp_port')
        self.smtp_user: str = Config.get('MAILER', 'smtp_user')
        self.smtp_password: str = Config.get('MAILER', 'smtp_password')

        _subject = Config.get('MAILER', 'Subject')
        _sender = Config.get('MAILER', 'sender')
        try:
            _receivers = Config.get('MAILER', 'receivers', param_type="json")
        except JSONDecodeError:
            Logger.get(self.__class__.__name__).warn('Problems decoding email receivers from JSON in config!')
            _receivers = None

        if not _subject or not _sender or not _receivers or not self.smtp_host or not self.smtp_port:
            Logger.get(self.__class__.__name__).warn('Emails not being sent!')
            return

        self.msg = EmailMessage()
        self.msg.set_charset('utf-8')
        self.msg['Subject'] = _subject
        self.msg['From'] = _sender
        self.msg['To'] = _receivers

        self.init_ok = True
