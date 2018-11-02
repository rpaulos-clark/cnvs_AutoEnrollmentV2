from request import Request
from councilconnect import CouncilConnect

# @TODO: Search for Placeholder comment to insert logging code once it exists


""" REQUIRES set up - must pass the authorization token and the base_url through method calls for CouncilConnect.
    Must also include the alert recipient for anyone to be alerted to any errors/hiccups the program may experience.
"""


class UserManager(CouncilConnect):

    @classmethod
    def delete_user(cls, ccID):
        try:
            req = Request.request(
                'delete',
                super().base_url+'api/v1/accounts/'+super().account()+'/users/',
                headers=super().council_headers)
            if 200 == req.status_code:
                print('Successfully deleted')
            else:
                ...
        except Exception as e:
            super().alert('Encountered exception {} while deleting user')

    @classmethod
    def create_user(cls, pseudonym_unique_id, sis_user_id, user_real_first, user_real_last):
        """
            Creates or reactivates (if the options remains uncommented) a user account on Council Connect.
            Returns None in the event the request response code != 200

        :param pseudonym_unique_id: this + @clark.edu becomes their login
        :param sis_user_id: unique identifier. PersonID in prometheus
        :param user_real_first:
        :param user_real_last:
        :return: requests Response object or None in the event of an exception
        """

        payload = {
            'user[name]': user_real_first + " " + user_real_last,
            'user[short_name]': user_real_first + " " + user_real_last,
            'user[sortable_name]': user_real_last + "," + " " + user_real_first,
            'pseudonym[unique_id]': pseudonym_unique_id + '@clark.edu',  # ID that will be used to log into the site
            'pseudonym[sis_user_id]': sis_user_id,  # Unique employee identifier. PersonID in prometheus

            """ Due to how often these accounts are potentially being reactivated, I am going to disable the 
                notification about account creation. We can probably get around this by tracking the latest CCID value 
                and, if the value is higher, send confirmation:true else false.

            """
            # Sends user an email letting them know of account creation (even upon SIS reactivation)
            # 'pseudonym[send_confirmation': 'True', 
            
            # Automatically marks user as registered, making their account established and allowing notifications to be 
            # sent, even without logging in
            'user[skip_registration]': 'True',
            'communication_channel[type]': 'email',

            # The email address the user is contacted at
            'communication_channel[address]': pseudonym_unique_id + '@clark.edu',

            # Allows notifications to be sent to the user even if they don't log in
            'communication_channel[skip_confirmation]': 'True',
            'enable_sis_reactivation': 'True'  # Reactivates a deleted account if the SIS IDs match
        }

        try:
            creation_request = Request.request(
                'post', super().base_url+'api/v1/accounts/'+str(super().canvas_account)+'/users',
                headers=super().council_headers,
                params=payload)

            # Placing these here for the benefit of anyone who uses this as a one-off
            print(user_real_first+' '+user_real_last+' creation status code %s' % creation_request.status_code)
            if 200 != creation_request.status_code:
                super().alert('Failed to create user {} {}'.format(user_real_first, user_real_last))
                return None
            print(creation_request.json())

            # Placeholder for logging
            return creation_request  # Expect called to use Request.extract if the status_Code is amenable

        except Exception as e:
            super().alert(
                'Encountered exception {} during user creation for {} {}'.format(e, user_real_first, user_real_last))
            print('Encountered exception {} during user creation for {} {}'.format(e, user_real_first, user_real_last))
            return None

    @classmethod
    def search_person_id(cls, person_id):
        users_req = UserManager.retrieve_users()
        users = super().extract_json(users_req)

        # For the benefit of casual users we print the data
        for user in users:
            if user['sis_user_id'] == person_id:
                print(user)
                return user
        print('No such user found')
        return None

    @classmethod
    def retrieve_users(cls):
        """
        :return: requests Response object or None upon exception
        """

        payload = {
            'sort': 'username',
            'order': 'asc',
            'per_page': '100'
        }

        try:
            req = super().request(
                'GET',
                super().base_url+'api/v1/accounts/'+str(super().canvas_account)+'/users',
                params=payload)

            return req

        except Exception as e:
            print('Encountered exception {} attempting to retrieve user list'.format(e))
            super().alert('Encountered exception {} retrieving user list'.format(e))
            return None

    @classmethod
    def retrieve_user_info(cls, user_id):
        """
        :param user_id: unique Council Connect ID number
        :return: requests Response or None upon exception
        """

        try:
            req = super().request('GET', super().base_url+'api/v1/users/'+str(user_id))
            content = req.json()

            # In case a less-able person is at the helm.
            for thing in content:
                print(thing)
            return req

        except Exception as e:
            print('Failed to retrieve user info with response code {}'.format(r.status_code))
            super().alert('Encountered exception {} retrieving user info for {}'.format(e, user_id))
            return None

