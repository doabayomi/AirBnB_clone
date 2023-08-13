#!/usr/bin/python3
""" this is the user module """

from models.base_model import BaseModel


class User(BaseModel):
    """ class User """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
