from rest_framework.exceptions import APIException


class NotFound(APIException):
    """
    Provide default 404 status code
    """
    status_code = 404


exception_message = {
    'article_does_not_exist': "Article does not exist. "
                                   "Check provided Article slug."
}


class IncorrectValues(APIException):
    """
    Provide default 400 status code
    """
    status_code = 400
    