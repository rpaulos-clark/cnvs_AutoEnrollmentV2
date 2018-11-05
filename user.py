from councilconnect import CouncilConnect


# Where are we going to store isPublished, listDiscussionTopics, discussionsHidden, update_enrollments,
# discussionSubscriptions, replaceCommChannel, editLogin, credentialCheck,


""" ListDiscussionTopics, editLogin, replaceCommChannel, discussionSubscriptions, updateEnrollments
"""


class User(CouncilConnect):

    def __init__(self, cc_id, name, sis_user_id, login_id):
        self.cc_id = cc_id
        self.name = name
        self.sis_user_id = sis_user_id
        self.login_id = login_id

    def edit_login(self, new_login):

        """
            Modifes what is essentially the username, the field used to log into Council Connect.  A user CAN have
            multiple logins. This method simply changes the first one it receives. Nothing more

        :param new_login: login that will be used to log into Council Connect. Delete the old.
        :return: Bool indicating success/failure
        """

        # First the user's credentials are retrieve so that they may be edited
        req = super().request('GET', super().base_url+'api/v1/users/'+str(self.cc_id)+'/logins')
        if 200 == req.status_code:
            login = req.json()[0]  # Returns list of logins. Only need to modify one (and they should have only one)
            old_login = login['id']

            params = {
                'login[unique_id]': new_login
            }

            # Now the login is updated
            req = super().request(
                'PUT',
                super().base_url+'api/v1/accounts/'+str(super().canvas_account)+'/logins/'+str(old_login),
                params=params)

            if 200 == req.status_code:
                self.login_id = new_login
                #//// Add logging here
                return True

        super().error_dump('Failed to update login for <{}> with response code <{}>'.format(new_login, req.status_code))
        return False

    def discussion_topics(self, course_id):
        # Lists the Discussion threads in the given course. Used to keep users subscribed and receiving their 'digests'
        # of discussion activity on Council Connect
        """

        :param course_id: id of the target course
        :return: list of discussion objects (dictionaries) or None upon request failure. The list can be empty
        """
        payload = {
            'order_by': 'title',
            'scope': 'unlocked',
            'as_user_id': 'sis_user_id:' + str(self.sis_user_id)  # Enables details from the user's perspective
        }

        req = super().request(
            'GET', super().base_url+'api/v1/courses/'+str(course_id)+'/discussion_topics', params=payload)

        if 200 == req.status_code:
            return super().extract_json(req)

        super().error_dump('Status code <{}> while retrieving discussions for <{}>'.format(req.status_code, self.name))
        return None



