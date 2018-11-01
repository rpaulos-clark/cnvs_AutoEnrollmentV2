from request import Request
from councilconnect import CouncilConnect

""" REQUIRES set up - must pass the authorization token and the base_url through method calls for CouncilConnect.
    Must also include the alert recipient for anyone to be alerted to any errors/hiccups the program may experience.
"""


class UserManager(CouncilConnect):

    @classmethod
    def retrieve_users(cls):
        """
        :return: Returns a list of user objects returned from the canvas api call or None if the status_code != 200
        """

        payload = {
            'sort': 'username',
            'order': 'asc',
            'per_page': '100'
        }
        headers = super().council_headers
        base_url = super().base_url
        account = super().canvas_account

        req = Request.request(
                'get', base_url+'api/v1/accounts/'+str(account)+'/users', headers=headers, params=payload)

        if 200 == req.status_code:
            user_list = Request.extract(headers, payload, req)
        else:
            return None

        return user_list

    @classmethod
    def retrieve_user_info(cls, user_id):
        """

        :param user_id: unique Council Connect ID number
        :return: user info object or None should the response_code != 200
        """

        r = Request.request('get', super().base_url+'api/v1/users/'+str(user_id), headers=super().council_headers)
        if 200 == r.status_code:
            return r.json()
        return None

