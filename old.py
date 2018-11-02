import os
import requests
import councilConnect

CCtoken = os.getenv('CCtoken')
CC_base_url = "https://councils.clark.edu/"
headers = {'Content-Type': 'application/json', 'Authorization': "Bearer " + CCtoken}


# Retrieve and print all User objects on Canvas by "account". Retrieves user objects
##########################################################################################################################
def retrieve_all_user_objects(account_number):

    """
    :param account_number: Integer representing the "account" on our Canvas site.


    :return: A list of dictionaries. Each dictionary is a user object
    """

    user_object_list = []

    # Alphabetizes returned user data
    payload = {
        'sort': 'username',
        'order': 'asc',
        'per_page': '100'
}

    # Pulls information from Canvas into request object r
    r = requests.get(CC_base_url + "/api/v1/accounts/" + str(account_number) + "/users", headers=headers, params=payload)

    #Loads the data returned from Canvas into "content"
    content = r.json()

    i = 0
    #Prints user information to console
    for users in content:
        i += 1
        user_object_list.append(users)
        #print(users)

    #Loads paginated user data from Canvas and returns the list
    while r.links['current']['url'] != r.links['last']['url']:
        request_url = r.links['next']['url']
        r = requests.get(request_url, headers=headers, params=payload)
        content = r.json()
        for users in content:
            i += 1
            user_object_list.append(users)
           # print(users)

    return user_object_list
#########################################################################################################################


def retrieve_user_info(user_id):

    r = requests.get(CC_base_url + "/api/v1/users/" + str(user_id), headers=headers)

    content = r.json()
    return content


# Create a user on Council Connect!
########################################################################################################################
def createUser(pseudonym_unique_id, sis_user_id, user_real_first, user_real_last):
    """

    :param pseudonym_unique_id:     This is what becomes their login id + @clark.edu
    :param sis_user_id:             UUID used to track employees
    :param user_real_first:
    :param user_real_last:
    :return:
    """

    payload = {
        'user[name]': user_real_first + " " + user_real_last,
        'user[short_name]': user_real_first + " " + user_real_last,
        'user[sortable_name]': user_real_last + "," + " " + user_real_first,
        'pseudonym[unique_id]': pseudonym_unique_id + '@clark.edu',  # ID that will be used to log into the site
        'pseudonym[sis_user_id]': sis_user_id,  # Unique employee identifier

        """ Due to how often these accounts are potentially being reactivated, I am going to disable the notification 
            about account creation. We can probably get around this by tracking the latest CCID value and, if the
            value is higher, send confirmation:true else false.

        """
        # 'pseudonym[send_confirmation': 'True', # Sends user an email letting them know of account creation (even upon SIS reactivation)
        'user[skip_registration]': 'True',
    # Automatically marks user as registered, making their account established and allowing notifications to be sent, even without logging in
        'communication_channel[type]': 'email',
        'communication_channel[address]': pseudonym_unique_id + '@clark.edu',
    # The email address the user is contacted at
        'communication_channel[skip_confirmation]': 'True',
    # Allows notifications to be sent to the user even if they don't log in
        'enable_sis_reactivation': 'True'  # Reactivates a deleted account if the SIS IDs match
    }

    # Canvas "account" number is hardcoded as 1
    try:
        user_creation_request = requests.post(CC_base_url + "/api/v1/accounts/1/users", headers=headers, params=payload)
        print(
            user_real_first + " " + user_real_last + " creation status code " + str(user_creation_request.status_code))
        content = user_creation_request.json()
        print(content)

        # with open("C:\Council Connect Logging/userCreationLogs/creationSuccess.txt", 'a', encoding='utf-8',
        #           errors='ignore') as logFile:
        #     logFile.write(str(datetime.datetime.now()) + " Successfully created CC account for " + str(
        #         user_real_first) + ' ' + str(user_real_last) +
        #                   ' ' + str(sis_user_id) + ' ' + str(content['id']) + '\n\n')
        return content
    except Exception as e:
        # with open("C:\Council Connect Logging/userCreationLogs/creationFailure.txt", 'a', encoding='utf-8',
        #           errors='ignore') as logFile:
        #     logFile.write(
        #         str(datetime.datetime.now()) + " Failed to create CC account for " + str(user_real_first) + ' ' + str(
        #             user_real_last) + ' ' +
        #         str(sis_user_id) + " with exception: " + str(e) + '\n\n')
        return None