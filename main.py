from councilconnect import CouncilConnect
from usermanager import UserManager
import os

import usermanager


if __name__ == "__main__":

    CouncilConnect.alert_recipient('RPaulos@clark.edu')
    #CouncilConnect.alert_recipient('ryan.eliopoulos@clark.edu')
    CouncilConnect.url('https://councils.clark.edu/')
    CouncilConnect.token(os.getenv('CCtoken'))

    CouncilConnect.alert('ohmygoodness')
    #users = UserManager.retrieve_users()

