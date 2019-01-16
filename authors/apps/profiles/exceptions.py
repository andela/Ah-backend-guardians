from rest_framework.exceptions import APIException
from rest_framework import status


class ProfileDoesNotExist(APIException):
    status_code = 404
    default_detail = "Profile does not exist. Check provided username."


class UserCannotEditProfile(APIException):
    status_code = 403
    default_detail = "Sorry, you cannot edit another users profile "


exception_messages = {
    'edit_profile_not_permitted': "You are not authorised to edit {0}'s \
profile"
}
