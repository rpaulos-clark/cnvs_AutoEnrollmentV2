import smtplib
import os
import time
"""
    Hope: this class will be a superclass for the top-level objects interacting with Council Connect. This will provide
    the subclasses the inherent ability to do things like send alert emails when something fails, etc.
"""


class CouncilConnect(object):
    base_url = None
    cc_token = None
    council_headers = None
    recipient = None
    canvas_account = 1

    @classmethod
    def alert(cls, message):
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        email_password = os.getenv('CouncilConnectTools')
        s.login("CouncilConnectTools@gmail.com", email_password)
        s.sendmail('CouncilConnectTools@gmail.com', cls.recipient, message)

    @classmethod
    def account(cls, account):
        CouncilConnect.canvas_account = account

    @classmethod
    def alert_recipient(cls, email):
        cls.alert_recipient = email

    @classmethod
    def url(cls, url):
        cls.base_url = url

    @classmethod
    def token(cls, token):
        cls.cc_token = token
        cls.council_headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + token}
