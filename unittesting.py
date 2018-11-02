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
        CouncilConnect.alert_recipient('rpaulos@clark.edu')
        CouncilConnect.alert('UnitTesting')

    def test_alert_recipients_added(self):
        CouncilConnect.alert_recipient('rpaulos@clark.edu')
        rep_list = 'rpaulos@clark.edu'
        self.assertEqual(rep_list, CouncilConnect.recipient)

    def test_url_method(self):
        CouncilConnect.url('penguins')
        self.assertEqual(CouncilConnect.base_url, 'penguins')

    def test_token_method(self):
        CouncilConnect.token('cheese')
        self.assertEqual(CouncilConnect.cc_token, 'cheese')

    def test_account_method(self):
        CouncilConnect.account(5)
        self.assertEqual(CouncilConnect.canvas_account, 5)

    def tearDown(self):
        CouncilConnect.base_url = 'https://councils.clark.edu/'
        CouncilConnect.cc_token = os.getenv('CCtoken')
        CouncilConnect.canvas_account = 1


class TestUserManager(unittest.TestCase):

    def setUp(self):
        CouncilConnect.init_session()

    def test_retrieve_users_against_original_functions(self):
        user_manager_data = UserManager.retrieve_users()
        ret_data = old.retrieve_all_user_objects(1)
        self.assertEqual(user_manager_data, ret_data)

    def test_retrieve_user_info_vs_original(self):
        # User ID of Ryan Paulos
        user_manager_data = UserManager.retrieve_user_info(12)
        ret_data = old.retrieve_user_info(12)
        self.assertEqual(user_manager_data, ret_data)

    def test_create_user(self):
        ret = UserManager.create_user('testosteroni', '@!!$testosteroni', 'test', 'osterone')
        if ret:
            ret = UserManager.create_user('testosteroni', '@!!$testosteroni', 'test', 'osterone')
        self.assertEqual(ret, None)

    def test_search_person_id(self):
        # Person ID of Ryan Paulos
        ret = UserManager.search_person_id('1EF69564-83D7-463A-B3F7-F1CFAA076554')
        self.assertEqual(ret['id'], 12)

        ret = UserManager.search_person_id('@!!$testosteroni')

    def test_delete_person(self):
        # user is created
        UserManager.delete_user(3081)
        search = UserManager.search_person_id(3081)
        self.assertEqual(None, search)

    def tearDown(self):
        UserManager.create_user('testosteroni', '@!!$testosteroni', 'test', 'osterone')


if __name__ == "__main__":
    unittest.TestSuite()
