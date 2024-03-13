import os
# username = os.environ['MY_USER']
# password = os.environ['MY_PASS']
# print("Running with user: %s" % username)
USERNAME = os.getenv('PASSWORD', 'test')
print(USERNAME)