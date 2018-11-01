import unittest
import os
from request import Request
from usermanager import UserManager
import old

from councilconnect import CouncilConnect

CCtoken = os.getenv('CCtoken')
CC_base_url = "https://councils.clark.edu/"
headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + CCtoken}


class TestCouncilConnect(unittest.TestCase):

    def test_alert(self):
        CouncilConnect.alert_recipients = ['rpaulos@clark.edu']
        CouncilConnect.alert('UnitTesting')

    def test_alert_recipients_added(self):
        CouncilConnect.alert_recipient('rpaulos@clark.edu')
        rep_list = 'rpaulos@clark.edu'
        self.assertEqual(rep_list, CouncilConnect.alert_recipient)

    def test_url_method(self):
        CouncilConnect.url('penguins')
        self.assertEqual(CouncilConnect.base_url, 'penguins')

    def test_token_method(self):
        CouncilConnect.token('cheese')
        self.assertEqual(CouncilConnect.cc_token, 'cheese')
        self.assertEqual(
            CouncilConnect.council_headers, {'Content-Type': 'application/json', 'Authorization': "Bearer " + 'cheese'})

    def test_account_method(self):
        CouncilConnect.account(5)
        self.assertEqual(CouncilConnect.canvas_account, 5)

    def tearDown(self):
        CouncilConnect.alert_recipients = []
        CouncilConnect.base_url = None
        CouncilConnect.cc_token = None
        CouncilConnect.canvas_account = 1


class TestRequest(unittest.TestCase):

    # Not really a great test
    def test_Request_against_retrieve_users(self):
        payload = {
            'sort': 'username',
            'order': 'asc',
            'per_page': '100'
        }
        r = Request.request('get', CC_base_url+'api/v1/accounts/1/users/', headers=headers, params=payload)
        users = Request.extract(headers, payload, r)
        ret = old.retrieve_all_user_objects(1)
        self.assertEqual(users, ret)


class TestUserManager(unittest.TestCase):

    def setUp(self):
        CouncilConnect.url('https://councils.clark.edu/')
        CouncilConnect.token(os.getenv('CCtoken'))

    def test_retrieve_users_against_original_functions(self):
        user_manager_data = UserManager.retrieve_users()
        ret_data = old.retrieve_all_user_objects(1)
        self.assertEqual(user_manager_data, ret_data)

    def test_retrieve_user_info_vs_original(self):
        user_manager_data = UserManager.retrieve_user_info(12)
        ret_data = old.retrieve_user_info(12)
        self.assertEqual(user_manager_data, ret_data)



if __name__ == "__main__":
    unittest.TestSuite()
