#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from app.mailer import Mailer
from app.template import TestMailTemplate

Mailer.send(TestMailTemplate(), "Test Email")
