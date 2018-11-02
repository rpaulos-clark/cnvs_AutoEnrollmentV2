import smtplib
import requests
import os
import time
"""
    Hope: this class will be a superclass for the top-level objects interacting with Council Connect. This will provide
    the subclasses the inherent ability to do things like send alert emails when something fails, etc.
"""


class CouncilConnect(object):
    base_url = 'https://councils.clark.edu/'
    cc_token = os.getenv('CCtoken')
    recipient = None
    request_session = None
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
        cls.recipient = email

    @classmethod
    def url(cls, url):
        cls.base_url = url

    @classmethod
    def token(cls, token):
        cls.cc_token = token

    @classmethod
    def init_session(cls):
        """
            Facilitates requests made by CouncilConnect subclasses
        """

        req_session = requests.Session()
        req_session.headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + cls.cc_token}
        cls.request_session = req_session

    @classmethod
    def request(cls, mode, url, params=None):
        """
            So we may benefit from the saved headers
        :param mode: 'GET', 'POST', etc
        :param url: Full API url
        :param params:
        :return: requests Response object
        """
        return cls.request_session.request(mode, url, params)

    @classmethod
    def extract_json(cls, req):
        """
        :param req: requests Response object
        :return: list of all values provided by the server
        """

        content = req.json()
        if not isinstance(content, list):
            content = [content]

        if req.links['current']['url'] == req.links['last']['url']:
            return content

        next_url = req.links['next']['url']
        content += cls.extract_json(cls.request('GET', next_url))
        return content
