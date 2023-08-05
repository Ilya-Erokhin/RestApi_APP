import hmac
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endoint
    with their username and password.
    :param username: User's username in string format.
    :param password: User's un-encryped password in string format.
    :return: A UserModel object if authentication was successful, None otherwise.
    """
    user = UserModel.find_by_username(username)

# If user was finded and both passwords are indentical, then we return the user, if NOT, we return the NONE
    if user and hmac.compare_digest(user.password, password):
        return user
    return None

def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT
    verified their authorization header is correct.
    :param payload: A dictionary with 'identity' key, which is user id.
    :return: A UserModel object.
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)