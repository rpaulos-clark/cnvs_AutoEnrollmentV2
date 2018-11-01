import unittest
import os
from request import Request
import old

from councilconnect import CouncilConnect

CCtoken = os.getenv('CCtoken')
CC_base_url = "https://councils.clark.edu/"
headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + CCtoken}


class TestCouncilConnect(unittest.TestCase):

    #def setUp(self):

    def test_alert_recipients_added(self):
        CouncilConnect.alert_recipient('rpaulos@clark.edu')
        CouncilConnect.alert_recipient('jrobertson@clark.edu')
        rep_list = ['rpaulos@clark.edu', 'jrobertson@clark.edu']
        self.assertEqual(rep_list, CouncilConnect.alert_recipients)

    def test_url_method(self):
        CouncilConnect.url('penguins')
        self.assertEqual(CouncilConnect.base_url, 'penguins')

    def test_token_method(self):
        CouncilConnect.token('cheese')
        self.assertEqual(CouncilConnect.cc_token, 'cheese')
        self.assertEqual(
            CouncilConnect.council_headers, {'Content-Type': 'application/json', 'Authorization': "Bearer " + 'cheese'})

    def tearDown(self):
        CouncilConnect.alert_recipients = []
        CouncilConnect.base_url = None
        CouncilConnect.cc_token = None


class TestRequest(unittest.TestCase):

    def test_request_against_retrieve_users(self):
        payload = {
            'sort': 'username',
            'order': 'asc',
            'per_page': '100'
        }
        r = Request.request('get', CC_base_url+'api/v1/accounts/1/users/', headers=headers, params=payload)
        users = Request.extract(headers, payload, r)
        ret = old.retrieve_all_user_objects(1)
        self.assertEqual(users, ret)



if __name__ == "__main__":
    unittest.main()
