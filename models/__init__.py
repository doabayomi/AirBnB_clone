#!/usr/bin/python3
""" this is the init for airbnb_clone storage engine """

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
