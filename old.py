import os
import requests


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
