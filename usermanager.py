import requests
from councilconnect import CouncilConnect
import os

""" REQUIRES set up - must pass the authorization token and the base_url through method calls
"""


class UserManager(CouncilConnect):


    @classmethod
    def retrieve_users(cls, account):
        """

        :param account: Canvas term. Almost certainly will always be 1.
        :return: Returns a
        """

        def paginate():


        payload = {
            'sort': 'username',
            'order': 'asc',
            'per_page': '100'
        }

        user_list = None
        try:
            user_request = cls.request('get', '/api/v1/accounts/{}/users'.format(account), params=payload)
            user_list = ancillary.paginate(user_request)
        except Exception as e:
            print("Exception {} while attempting to retrieve users".format(e))

        return user_list




