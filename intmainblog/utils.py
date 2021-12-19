def get_filename(filename, request):
    return filename.upper()


def isValidUsername(username):
    names = ['user', 'user1', 'user2', 'user3 ', 'user4' 'name',
             'myname', 'nickname', 'admin', 'adminstrator']
    if not username in names:
        return True
    return False
