#!/usr/bin/python3
""" this is the file storage engine room """

import json

import models
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State


class FileStorage:
    """ class Filestorage """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the object"""

        return self.__objects

    def new(self, obj):
        """ creates a new instance witha unique id """

        class_name = obj.__class__.__name__
        obj_id = obj.id
        key = f"{class_name}.{obj_id}"
        self.__objects[key] = obj

    def save(self):
        """ saves the instance """

        with open(self.__file_path, "w") as json_file:
            self.__objects = {key: obj if isinstance(obj, dict) else
                              obj.to_dict() for key, obj in
                              self.__objects.items()}
            json.dump(self.__objects, json_file)

    def reload(self):
        """ reload back to a json string into the file """

        try:
            try:
                with open(self.__file_path, mode='r') as my_file:
                    new_dict = json.load(my_file)

                for key, value in new_dict.items():
                    class_name = value.get('__class__')
                    obj = eval(class_name + '(**value)')
                    self.__objects[key] = obj

            except json.JSONDecodeError:
                # Handle JSON decoding errors if needed
                pass
        except FileNotFoundError:
            pass
