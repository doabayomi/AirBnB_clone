#!/usr/bin/python3
""" this is the base_model that does the initializing function """

import uuid
import models
from datetime import datetime


class BaseModel:
    """ the is the mother BaseModel class """

    def __init__(self, *args, **kwargs):
        """class constructor for class BaseModel"""

        if kwargs:
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')

            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """ that prints a class name then id and then the dict"""

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """ that saves the instance """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ converts to dictionary """

        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__

        if 'created_at' in obj_dict:
            obj_dict['created_at'] = obj_dict['created_at'].isoformat()

        if 'updated_at' in obj_dict:
            obj_dict['updated_at'] = obj_dict['updated_at'].isoformat()

        return obj_dict
