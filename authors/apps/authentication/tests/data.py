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

# test data for test_view.py

user1 = {
    "user": {
        "username": "makabugo",
        "email": "makabugo@andela.com",
        "password": "Simulman2101"
        }
    }

user2 = {
    "user": {
        "username": "fahad12",
        "email": "fahad.mak@andela.com",
        "password": "andela13"
        }
    }

login_info = {
    "user": {
        "email": "fahad.mak@andela.com",
        "password": "andela13"
        }
    }

user_update = {
    "user": {
        "username": "mark12",
        "email": "guardiansed.sims@andela.com",
        "password": "simulman2101"
        }
    }

short_password = {
    "user": {
        "username": "testuser",
        "email": "testsims@andela.com",
        "password": "test"
        }
    }

invalid_username = {
    "user": {
        "username": "tes()",
        "email": "testsims@andela.com",
        "password": "Test@567"
        }
    }
poor_conventions_password = {
    "user": {
        "username": "testuser",
        "email": "test.sims@andela.com",
        "password": "testerrrr"
        }
    }

short_username = {
    "user": {
        "username": "tes",
        "email": "test.sims@andela.com",
        "password": "Test@567"
        }
    }

incorrect_email = {
            "user": {
                "email": "kamira@ymai.co"
            }
        }

userp = {
            "user": {
                'email': "moses@gmail.com",
                'username': "mosesk",
                'password': "Moses123"
            }
        }

email = {
            "user": {
                "email": "moses@gmail.com"
            }
        }
password = {
            "password": "MosesKamira123",
            "confirm_password": "MosesKamira123"
        }

no_email = {
            "user": {
                "email": ""
            }
        }
