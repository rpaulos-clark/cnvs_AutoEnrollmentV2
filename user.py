from councilconnect import CouncilConnect


# Where are we going to store isPublished, listDiscussionTopics, discussionsHidden, update_enrollments,
# discussionSubscriptions, replaceCommChannel, editLogin, credentialCheck,


"""   discussionSubscriptions
"""


class User(CouncilConnect):

    inaccessible_discussions = []  # Will be skipped when

    def __init__(self, cc_id, name, sis_user_id, login_id):
        self.cc_id = cc_id
        self.name = name
        self.sis_user_id = sis_user_id
        self.login_id = login_id
        self.enrollments = []  # Ints of courses the user is enrolled in. Populated by update_enrollments()

    def discussion_subscription(self):
        """
             Subscribes user to all of the open discussions for courses in which they are enrolled.
        :return: None
        """
        self.update_enrollments()  # Ensure we have the entire list of user's courses

        # Like and subscribe
        for course in self.enrollments:

            # If inaccessible
            if not self.is_subscribable(course):
                User.inaccessible_discussions.append(course)

            # Discussions are accessible
            else:
                course_discussions = self.list_discussion_topics(course)

                if course_discussions is not None:  # There are discussions that can be subscribed to

                    # So subscribe to them all
                    for discussion in course_discussions:
                        if not discussion['subscribed']:  # unless the user is already subscribed

                            payload = {
                                'as_user_id': 'sis_user_id:{}'.format(self.sis_user_id)
                            }
                            req = super().request(
                                'PUT',
                                super().base_url+'api/v1/courses/{}/discussion_topics/{}/subscribed'.format(
                                    course, discussion['id']),
                                params=payload)

                            if req.status_code != 200 and req.status_code != 204:
                                super().error_dump(
                                    'Failed to subscribe <{}> to course <{}> with status code <{}>'.format(
                                        self.name, course, req.status_code))

    def list_discussion_topics(self, course_id):
        """
            Helper subroutine for discussion_subscription method
        :param course_id: int representation of the desired canvas course
        :return: List of discussions (threads) that the user is subscribed to, or None upon failure
        """

        payload = {
            'order_by': 'title',
            'scope': 'unlocked',
            'as_user_id': 'sis_user_id:{}'.format(self.sis_user_id)  # We need the details from the user's perspective
        }

        req = super().request(
            'GET', super().base_url+'api/v1/courses/{}/discussion_topics'.format(course_id), params=payload)

        if 200 != req.status_code:
            super().error_dump(
                'Failed to retrieve discussions for <{}> with status code <{}>'.format(self.name, req.status_code))
            return None
        content = super().extract_json(req)
        discussions = []

        for post in content:
            discussions.append(post)

        return discussions

    def is_subscribable(self, course_id):
        """
            Helper subroutine for discussion_subscription method. Filters out scenarios in which no discussion topics
            will be returned by an API call.
        :param course_id: Int value of the corresponding course
        :return: Bool
        """
        if course_id in User.inaccessible_discussions:
            return False
        if not super().is_published(course_id):
            return False
        if super().is_discussion_hidden(course_id):
            return False

        return True

    def update_enrollments(self):
        """
            updates self.enrollments with integer values corresponding to the course_id of each course the user is
            enrolled in.

        :return: None
        """
        # Retrieve the enrollments
        req = super().request('GET', super().base_url+'api/v1/users/{}/enrollments'.format(self.cc_id))
        if 200 != req.status_code:
            super().error_dump(
                'Failed to update enrollments for <{}> with status code <{}>'.format(self.name, req.status_code))
            return

        # Update self
        enrollments = super().extract_json(req)
        for enrollment in enrollments:
            self.enrollments.append(enrollment['course_id'])

    def replace_comm_channel(self, replacement_email):
        """
            Deletes all (though there should be only one) communication methods a user has within Council Connect
            and replaces them with the given email address. All notifications are now sent to this address.

            Support for modalities outside of email were never considered.

        :param replacement_email: Address Council Connect will now send notifications, etc. to
        :return: Canvas CommunicationChannel upon success, otherwise None
        """
        # Retrieves list of comm channels
        req = super().request('GET', super().base_url+'api/v1/users/'+str(self.cc_id)+'/communication_channels')

        if 200 != req.status_code:
            super().error_dump(
                'Failed to retrieve comm channels for <{}> with status code <{}>'.format(self.name, req.status_code))
            return

        chans = req.json()  # The list of communication channels, received as dictionaries

        # Delete all comm channels
        for channel in chans:
            comm_id = channel['id']
            req = super().request(
                'DELETE', super().base_url+'api/v1/users/'+str(self.cc_id)+'/communication_channels/'+str(comm_id))

            if 200 != req.status_code:
                super().error_dump(
                    'Error deleting comm channel for <{}> with status code <{}>'.format(self.name, req.status_code))
                return

        # Now for the creation of the new comm channel
        payload = {
            'communication_channel[address]': replacement_email,
            'communication_channel[type]': 'email',
            'skip_confirmation': 'True'
        }

        # Request for creation
        req = super().request(
            'POST',
            super().base_url+"api/v1/users/{}/communication_channels".format(self.cc_id),
            params=payload)

        if 200 == req.status_code:
            return req.json()
        super().error_dump(
            'Failed to create new comm channel for <{}> with response code <{}>'.format(self.name, req.status_code))

    def edit_login(self, new_login):

        """
            Modifes what is essentially the username, the field used to log into Council Connect.  A user CAN have
            multiple logins. This method simply changes the first one it receives. Nothing more.


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

