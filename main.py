from councilconnect import CouncilConnect
from usermanager import UserManager
import os

import usermanager


if __name__ == "__main__":

    #CouncilConnect.url('https://councils.clark.edu/')  # The trailing slash is required
    #CouncilConnect.token(os.getenv('CCtoken'))  # Will require explanation in the docs
    CouncilConnect.alert_recipient('RPaulos@clark.edu')  # where failure alerts will be sent
    CouncilConnect.init_session()  # Gets things ready. MUST be called.

    #user = UserManager.search_person_id('@!!$testosteroni')
    #users = UserManager.retrieve_users()

    UserManager.search_person_id('@!!$testosteroni')