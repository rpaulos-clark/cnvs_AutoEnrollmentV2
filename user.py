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


    # def edit_login(self):

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



