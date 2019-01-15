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

user2 = {
    "username": "fahad12",
    "email": "fahad.mak@andela.com",
    "password": "andela13"
}

login_info = {
    "email": "fahad.mak@andela.com",
    "password": "andela13"
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
    "username": "fahad12",
    "email": "guardiansed.sims@andela.com",
    "password": "Simulman2101"
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
