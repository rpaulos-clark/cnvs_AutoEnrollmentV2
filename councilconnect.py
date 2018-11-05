import smtplib
import requests
import os
"""
    Hope: this class will be a superclass for the top-level objects interacting with Council Connect. This will provide
    the subclasses the inherent ability to do things like send alert emails when something fails, etc.
"""


class CouncilConnect(object):
    base_url = 'https://councils.clark.edu/'
    cc_token = os.getenv('CCtoken')
    recipient = 'rpaulos@clark.edu'
    request_session = None
    canvas_account = '1'

    @classmethod
    def is_discussion_hidden(cls, course_id):
        """
            Basically checking if discussions are enabled or not(hidden)

        :param course_id: Course for which discussions status is checked
        :return: Bool indicating whether the discussions are hidden
        """

        req = cls.request('GET', cls.base_url+'api/v1/courses/'+str(course_id)+'/tabs')
        content = cls.extract_json(req)
        for tab in content:
            if tab['id'] == 'discussions':
                try:
                    if tab['hidden']:
                        return True
                    else:
                        return False
                except KeyError:
                    return False

    @classmethod
    def is_published(cls, course_id):
        """
            Determines the published state of the given course
        :return: Bool
        """

        payload = {
            'published': 'true'
        }
        req = cls.request('GET', cls.base_url+'api/v1/accounts/'+str(cls.canvas_account)+'/courses', params=payload)

        if 200 == req.status_code:
            content = req.json()
            for course in content:
                if int(course['id']) == int(course_id):
                    return True
            return False

        cls.error_dump('Status code <{}> in is_published for course <{}>'.format(req.status_code, course_id))

    @classmethod
    def alert(cls, message):
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        email_password = os.getenv('CouncilConnectTools')
        s.login("CouncilConnectTools@gmail.com", email_password)
        s.sendmail('CouncilConnectTools@gmail.com', cls.recipient, message)

    @classmethod
    def account(cls, account):
        """
            In case the 'account' is no longer 1. 'account' here refers to some division feature within Canvas to
            allow different aspects of Canvas to operate in isolation. This will probably never be necessary.
        :param account: integer or string rep of an int
        :return: None
        """
        CouncilConnect.canvas_account = str(account)

    @classmethod
    def alert_recipient(cls, email):
        """
            To update the email account that will be blessed with lots of error alert messages
        :param email: Email address which will receive the error notifications when something goes wrong
        :return: None
        """
        cls.recipient = email

    @classmethod
    def url(cls, url):
        """
            Method to update the base_url used when forming API calls. Seems unlikely to change.
        :param url: the URL to the login screen of Council Connect
        :return: None
        """
        cls.base_url = url

    @classmethod
    def token(cls, token):
        """
            Allows for updating the access token (provided by and created through Canvas) used to make API calls.
            REQUIRED

        :param token: Access token permitted authorization of API calls
        :return:  None
        """
        cls.cc_token = token

    @classmethod
    def init_session(cls):
        """
            Facilitates requests made by CouncilConnect subclasses. MUST BE CALLED before attempting to do anything
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

        if not req.links:
            return content

        if req.links['current']['url'] == req.links['last']['url']:
            return content

        next_url = req.links['next']['url']
        content += cls.extract_json(cls.request('GET', next_url))
        return content

    @classmethod
    def error_dump(cls, message):
        """
            Duplicates message for both terminal printing and email alerting
        :param message: Failure message string
        :return: None
        """
        print(message)
        cls.alert(message)
