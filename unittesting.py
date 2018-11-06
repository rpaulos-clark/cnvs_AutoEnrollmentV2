import copy
import unittest
import user
import os
from usermanager import UserManager
import old

from councilconnect import CouncilConnect

CCtoken = os.getenv('CCtoken')
CC_base_url = "https://councils.clark.edu/"
headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + CCtoken}


class TestCouncilConnect(unittest.TestCase):

    def setUp(self):
        CouncilConnect.alert_recipient('councilconnecttest@gmail.com')
        CouncilConnect.init_session()

    def test_alert(self):
        CouncilConnect.alert_recipient('councilconnecttest@gmail.com')
        CouncilConnect.alert('UnitTesting')

    def test_alert_recipients_added(self):
        CouncilConnect.alert_recipient('councilconnecttest@gmail.com')
        rep_list = 'councilconnecttest@gmail.com'
        self.assertEqual(rep_list, CouncilConnect.recipient)

    def test_url_method(self):
        CouncilConnect.url('penguins')
        self.assertEqual(CouncilConnect.base_url, 'penguins')

    def test_token_method(self):
        CouncilConnect.token('cheese')
        self.assertEqual(CouncilConnect.cc_token, 'cheese')

    def test_account_method(self):
        CouncilConnect.account(5)
        self.assertEqual(CouncilConnect.canvas_account, '5')

    def test_is_published_method(self):
        # Guided Pathways Resource Center. Should be published
        self.assertEqual(True, CouncilConnect.is_published(13))

        # MyClark Course. Should be unpublished
        self.assertEqual(False, CouncilConnect.is_published(24))

    def test_is_discussion_hidden_method(self):
        # Current (as of 11/5/2018) Council course
        self.assertEqual(False, CouncilConnect.is_discussion_hidden(27))
        self.assertEqual(True, CouncilConnect.is_discussion_hidden(15))

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

    def test_delete_person(self):
        # user is created
        UserManager.delete_user(3081)
        search = UserManager.search_person_id(3081)
        self.assertEqual(None, search)

    def test_create_enrollment(self):
        # Enrolling Ryan Paulos into the accreditation course with 'Employee' permissions
        req = UserManager.create_enrollment(12, 15, 'TeacherEnrollment', 13)
        self.assertEqual(200, req.status_code)

    def tearDown(self):
        UserManager.create_user('testosteroni', '@!!$testosteroni', 'test', 'osterone')


class TestUser(unittest.TestCase):

    user = None

    def setUp(self):
        CouncilConnect.init_session()
        TestUser.user = user.User(3081, 'test osterone', '@!!$testosteroni', 'testosteroni@clark.edu')
        UserManager.create_enrollment(3081, 15, 'TeacherEnrollment', '13')
        UserManager.create_enrollment(3081, 1, 'TeacherEnrollment', '13')

    def test_discussion_topics_method(self):
        person = user.User(12, 'Ryan Paulos', '1EF69564-83D7-463A-B3F7-F1CFAA076554', 'rpaulos@clark.edu')

        # Pulls discussion topics from the accreditation course
        discussion = person.discussion_topics(15)[0]
        self.assertEqual(True, isinstance(discussion, dict))
        discussions = person.discussion_topics(24)
        self.assertEqual(len(discussions), 0)

    def test_user_edit_login(self):
        person = copy.deepcopy(TestUser.user)
        ret = person.edit_login('testosteroniIsKing')
        self.assertEqual(True, ret)
        tes = UserManager.search_person_id('@!!$testosteroni')
        self.assertEqual(tes['sis_login_id'], 'testosteroniIsKing')

    def test_user_replace_comm_channel(self):
        person = copy.deepcopy(TestUser.user)
        ret = person.replace_comm_channel('KingJames@clark.edu')
        self.assertEqual('KingJames@clark.edu', ret['address'])

    def test_user_update_enrollments(self):
        person = copy.deepcopy(TestUser.user)
        person.update_enrollments()

        enrolled = [1, 15]
        self.assertEqual(len(person.enrollments), 2)
        for course in person.enrollments:
            self.assertIn(course, enrolled)

    def tearDown(self):
        person = user.User(3081, 'test osterone', '@!!$testosteroni', 'testosteroni@clark.edu')
        person.edit_login('testosteroni@clark.edu')
        person.replace_comm_channel('testosteroni@clark.edu')


if __name__ == "__main__":
    unittest.TestSuite()
