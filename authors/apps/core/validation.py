from rest_framework.serializers import ValidationError
import re
import string


class ValidateRegistrationData:

    def password_validation(self, password):
        error = "Ensure password has an uppercase, lowercase, " \
                "a numerical character and no leading or " \
                "trailing spaces."
        regex = r'(?P<password>((?=\S*[A-Z])(?=\S*[a-z])(?=\S*\d)\S))'
        if (re.compile(regex).search(password) is None):
            raise ValidationError(error)

    def username_validation(self, username):
        error = "Ensure username has only letters, " \
                "numbers or a combination of both."
        error2 = "Ensure username is atleast 4 characters long."
        regex = r'^\w+$'
        if (re.compile(regex).search(username) is None):
            raise ValidationError(error)
        elif len(username) < 4:
            raise ValidationError(error2)
