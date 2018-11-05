from councilconnect import CouncilConnect


# Where are we going to store isPublished, listDiscussionTopics, discussionsHidden, update_enrollments,
# discussionSubscriptions, replaceCommChannel, editLogin, credentialCheck,




""" ListDiscussionTopics belongs to User
"""

class User(CouncilConnect):

    def __init__(self, cc_id, first_name, last_name, sis_id, login_id):
        self.cc_id = cc_id
        self.first_name = first_name
        self.last_name = last_name
        self.sis_id = sis_id
        self.login_id = login_id




