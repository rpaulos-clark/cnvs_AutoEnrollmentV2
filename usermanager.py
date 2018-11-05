from councilconnect import CouncilConnect

# @TODO: Search for Placeholder comment to insert logging code once it exists


""" REQUIRES set up - must pass the authorization token and the base_url through method calls for CouncilConnect.
    Must also include the alert recipient for anyone to be alerted to any errors/hiccups the program may experience.
"""


class UserManager(CouncilConnect):

    @classmethod
    def create_enrollment(cls, cc_id, course_id, enrollment_type, role_id):
        """

        :param cc_id: Council Connect ID
        :param course_id: Course into which the user is being enrolled
        :param enrollment_type: The permission type the role_id is based upon (e.g. 'StudentEnrollment')
        :param role_id: integer corresponding to a permission role
        :return: requests Response object or 0 upon exception
        """

        payload = {
            'enrollment[user_id]': cc_id,
            'enrollment[type]': enrollment_type,
            'enrollment[role_id]': role_id,
            'enrollment[enrollment_state]': 'active',
            # 'enrollment[notify]': 'true' # Too many notifications. No longer sending.
        }

        try:
            enrollment_request = super().request(
                'POST',
                super().base_url+'api/v1/courses/'+str(course_id)+'/enrollments',
                params=payload)

            if 200 != enrollment_request.status_code:
                super().error_dump(
                    'Failed to create enrollment for id:<{}> with status code <{}>'.format(
                        cc_id, enrollment_request.status_code))
            else:
                print('Successfully created new enrollment for id:{} in course {}'.format(cc_id, course_id))
            return enrollment_request
        except Exception as e:
            super().error_dump('Encountered exception <{}> while creating enrollment for id:{}'.format(e, cc_id))
            return 0

    @classmethod
    def delete_user(cls, cc_id):
        """
            Deactivates the given account. Can be reactivated, although at least the enrollments are lost.

        :param cc_id: Council Connect User ID
        :return: None
        """

        cc_id = str(cc_id)
        try:
            req = super().request(
                'DELETE',
                super().base_url+'api/v1/accounts/'+str(super().canvas_account)+'/users/'+cc_id
            )

            if 200 == req.status_code:
                print('Successfully deleted %s' % cc_id)
                return

            print('Encountered response code %s while attempting to delete cc_id:%s' % (req.status_code, cc_id))
        except Exception as e:
            super().error_dump('Encountered exception %s while attempting to delete cc_id:%s' % (e, cc_id))

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
            creation_request = super().request(
                'POST', str(super().base_url+'api/v1/accounts/'+str(super().canvas_account))+'/users', params=payload)
            if 200 != creation_request.status_code:
                super().error_dump('Failed to create user {} {} with status code {}'.format(
                    user_real_first, user_real_last, creation_request.status_code))
                return None
            #/// add logging here
            return creation_request.json()

        except Exception as e:
            super().error_dump(
                'Encountered exception <{}> during user creation for {} {}'.format(e, user_real_first, user_real_last))
            return None

    @classmethod
    def search_person_id(cls, person_id):
        """
            Retrieves all user objects from Council Connect and then searches through the list of users to find
            the given person.

        :param person_id: Person_ID field for employees within prometheus. Corresponds to sis_user_id in canvas terms
        :return: Canvas user object (dictionary) or None if no match is found
        """

        users = UserManager.retrieve_users()  # Already a list

        # For the benefit of casual users we print the data
        for user in users:
            if user['sis_user_id'] == person_id:
                for key, value in user.items():
                    print(str(key)+':'+str(value))
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
                payload)

            if 200 != req.status_code:
                super().error_dump('Failed to retrieve users. Status code %s' % req.status_code)
                return None
            return super().extract_json(req)

        except Exception as e:
            super().error_dump('Encountered exception <{}> attempting to retrieve user list'.format(e))
            return None

    @classmethod
    def retrieve_user_info(cls, user_id):
        """
        :param user_id: unique Council Connect ID number
        :return: requests Response or None upon exception
        """
        user_id = str(user_id)

        try:
            req = super().request('GET', super().base_url+'api/v1/users/'+str(user_id))

            if 200 != req.status_code:
                super().error_dump(
                    'Failed to retrieve info for user <{}> with status code <{}>'.format(user_id, req.status_code))
                return None
            content = req.json()

            # In case a less-able person is at the helm.
            for key, value in content.items():
                print(str(key)+':'+str(value))
            return content

        except Exception as e:
            super().error_dump('Encountered exception <{}> retrieving user info for <{}>'.format(e, user_id))
            return None
