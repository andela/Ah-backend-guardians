from django.conf import settings

# test data for test_model.py
user_data = {
    "username": "test",
    "email": "test@andela.com",
    "password": "Testma101"
}
user_data_no_username = {
    "username": None,
    "email": "test@andela23.com",
    "password": "Testma101"
}

user_data_no_email = {
    "username": "test",
    "email": None,
    "password": None
}

super_user_data = {
    "username": "freddert3",
    "email": "fahad.makabugo@an.com",
    "password": "Dann123"
}

super_user_data_no_username = {
    "username": None,
    "email": "fahad.makabugo@an.com",
    "password": "Dann123"
}

super_user_data_no_password = {
    "username": "freddert3",
    "email": "fahad.makabugo@an.com",
    "password": None
}

user1 = {
    "username": "makabugo",
    "email": "makabugo@andela.com",
    "password": "Simulman2101"
}
verify_user1 = {
    "msg": "Go to your email address to confirm registration",
    "route": "'/api/users/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
            eyJ1c2VybmFtZSI6Im1ha2FidWdvQGFuZGVsYS5jb20iLCJleHAiOiIxNTUyODEyNTc3In0.\
            jnTWF6LsEuqS6RtOFYXP4q61BzwCFOAhcUQa-TVnNAU/bWFrYWJ1Z28/'"
}

user2 = {
    "username": "Greenday",
    "email": "f.faraqhan@gmail.com",
    "password": "Mkdons1233"
}

user3 = {
    "username": "Greenday91234",
    "email": "f.faraqhan91234@gmail.com",
    "password": "Mkdons1239123"
}

user4 = {
    "username": "myrdstom",
    "email": "nserekopaul@gmail.com",
    "password": "Password1"
}

login_info = {
    "email": "f.faraqhan91234@gmail.com",
    "password": "Mkdons12391234"
}


inactive_login_info = {
    "email": "f.faraqhan9123@gmail.com",
    "password": "Mkdons1239123"
}

logged_in_user2 = {
    "username": "Greenday91234",
    "token": "khkcdjgs53779379"
}

bad_login_info1 = {
    "email": None,
    "password": None
}

bad_login_info2 = {
    "email": "",
    "password": ""
}

user_update = {
    "username": "Greenday91234",
    "email": "guardiansed.sims@andela.com"
}

short_password = {

    "username": "testuser",
    "email": "testsims@andela.com",
    "password": "test"

}

invalid_username = {
    "username": "tes()",
    "email": "testsims@andela.com",
    "password": "Test@567"

}

poor_conventions_password = {

    "username": "testuser",
    "email": "test.sims@andela.com",
    "password": "testerrrr"

}

incorrect_email = {
    "email": "kamira@ymai.co"
}

userp = {
    'email': "moses@gmail.com",
    'username': "mosesk",
    'password': "Moses123"
}

email = {
    "email": "moses@gmail.com"
}
password = {
    "password": "MosesKamira123",
    "confirm_password": "MosesKamira123"
}

no_email = {
    "email": ""
}

short_username = {

    "username": "tes",
    "email": "test.sims@andela.com",
    "password": "Test@567"

}

inactive_account = {
    "error": 'Please go to your email, to activate your account'
}

active_account = {
    "email": "f.faraqhan91234@gmail.com",
}

decode_error = 'Invalid authentication. Could not decode token'

prefix_error = 'Bearer is expected as the prefix'

# Test Data for Social Login

wrong_fb_token = {
    "access_token": "wrong_fb_token"
}

fb_token = {
    'access_token': "correct_access_token"
}

google_token = {
    "access_token": "google_token"
}

twitter_token = {
    "access_token": "access_token",
    "access_token_secret": "access_token_secret"
}
