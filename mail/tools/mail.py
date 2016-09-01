# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import parseaddr, formataddr
import smtplib

class Mail():
    config = {
        'from'     : '',
        'password' : '',
        'to'       : [],
        'smtp'     : ''
    }

    def formatAddr(self, s):
        name, addr = parseaddr(s)
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def create(self, content):
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = self.formatAddr(u'小粉丝 <%s>' % self.config['from'])
        msg['To'] = self.formatAddr(u'小天才 <%s>' % self.config['to'][0])
        msg['Subject'] = Header(u'来自小粉丝的日常问候', 'utf-8').encode()
        self.msg = msg

    def send(self):
        server = smtplib.SMTP(self.config['smtp'], 25)
        server.set_debuglevel(1)
        server.login(self.config['from'], self.config['password'])
        server.sendmail(self.config['from'], self.config['to'], self.msg.as_string())
        server.quit()