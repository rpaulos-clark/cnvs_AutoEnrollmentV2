import smtplib
"""
    Hope: this class will be a superclass for the top-level objects interacting with Council Connect. This will provide
    the subclasses the inherent ability to do things like send alert emails when something fails, etc.
"""


class CouncilConnect(object):
    base_url = None
    cc_token = None
    council_headers = None
    alert_recipients = []  # List of email addresses

    @classmethod
    def alert(cls, message):
        s = smtplib.SMTP(host='smtpout.clark.edu')
        s.starttls()
        try:
            for recipient in cls.alert_recipients:
                s.sendmail('CouncilConnectTools@clark.ed', recipient, message)
        except Exception as e:
            print(
                "Error:{}  while attempting to send an alert email about "
                "another error with message:{}".format(e, message))

    @classmethod
    def alert_recipient(cls, email):
        cls.alert_recipients.append(email)

    @classmethod
    def url(cls, url):
        cls.base_url = url

    @classmethod
    def token(cls, token):
        cls.cc_token = token
        cls.council_headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + token}
