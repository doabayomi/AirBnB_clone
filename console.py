#!/usr/bin/python3
""" this is a console for airbnb_clone """

import cmd
import json
import re

import models

from models import FileStorage, storage
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State


class HBNBCommand(cmd.Cmd):
    """ interactive console """

    prompt = '(hbnb) '
    __valid_classes = {
        "BaseModel", "User", "State", "City",
        "Place", "Amenity", "Review"
    }

    def do_quit(self, line):
        "Quit command to exit the program"

        return True

    def do_EOF(self, line):
        "exit the program using Ctrl + d"

        return True

    def emptyline(self):
        '''dont execute anything when user
           press enter an empty line
        '''
        pass

    def do_create(self, line):
        "Create a new instance of the class called"

        if not line:
            print('** class name missing **')
        else:
            if line in HBNBCommand.__valid_classes:
                b = eval(line + '()')
                b.save()
                models.storage.reload()
                print(b.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, args):
        '''Prints the string representation of a specific instance
           Usage: show <class name> <id>
        '''
        strings = args.split()
        if len(strings) == 0:
            print("** class name missing **")
        elif strings[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
        elif len(strings) == 1:
            print("** instance id missing **")
        else:
            obj = storage.all()
            key_value = strings[0] + '.' + strings[1]
            if key_value in obj:
                print(obj[key_value])
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        '''Delete an instance
           Usage: destroy <class name> <id>
        '''
        args = args.split()
        objects = models.storage.all()

        if len(args) == 0:
            print('** class name missing **')
        elif args[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print('** instance id missing **')
        else:
            key_find = args[0] + '.' + args[1]
            if key_find in objects.keys():
                objects.pop(key_find, None)
                models.storage.save()
            else:
                print('** no instance found **')

    def do_all(self, args):
        '''Print a string representation of all instances
           Usage: all <class name>
        '''
        args = args.split()
        objects = models.storage.all()
        new_list = []

        if len(args) == 0:
            for obj in objects.values():
                new_list.append(obj.__str__())
            print(new_list)
        elif args[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
        else:
            for obj in objects.values():
                if obj.__class__.__name__ == args[0]:
                    new_list.append(obj.__str__())
            print(new_list)

    def do_update(self, args):
        '''update an instance
           Usage update <class name> <id> <attribute name> "<attribute value>"
        '''

        if not args:
            print("** class name missing **")
            return False
        objects = models.storage.all()
        args = args.split(" ")
        if args[0] not in HBNBCommand.__valid_classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        elif args[2] == "id" or args[2] == "created_at"\
                or args[2] == "updated_at":
            return
        else:
            key_find = args[0] + '.' + args[1]
            obj = objects.get(key_find, None)

            if not obj:
                print("** no instance found **")
                return
            if args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtype(args[3].lstrip('"')
                                                       .rstrip('"'))
                models.storage.save()
                models.storage.reload()
            else:
                obj.__dict__[args[2]] = args[3].lstrip('"').rstrip('"')
            models.storage.save()
            models.storage.reload()

    def default(self, item):
        """ Default options """
        objects = models.storage.all()
        new_list = []

        keys = re.split(r'\.|\(\)|\(|\)|, ', item)
        if keys[0] not in self.__valid_classes:
            print("** class doesn't exist **")
            return
        if keys[0] in self.__valid_classes and keys[1] == "all":
            for obj in objects.values():
                if obj.__class__.__name__ == keys[0]:
                    new_list.append(obj.__str__())
            formatted_output = ", ".join(new_list)
            print("[" + formatted_output + "]")
        elif keys[0] in self.__valid_classes and keys[1] == "count":
            class_name = keys[0]
            count = sum(1 for obj in objects.values() if
                        obj.__class__.__name__ == class_name)
            print(count)
        elif keys[0] in self.__valid_classes and keys[1] == "show":
            s_id = keys[2].lstrip('"').rstrip('"')
            key_value = f'{keys[0]}.{s_id}'
            if key_value in objects:
                print(objects[key_value])
            else:
                print('** no instance found **')
        elif keys[0] in self.__valid_classes and keys[1] == "destroy":
            s_id = keys[2].lstrip('"').rstrip('"')
            key_value = f'{keys[0]}.{s_id}'
            if key_value in objects:
                objects.pop(key_value, None)
                models.storage.save()
                models.storage.reload()
            else:
                print('** no instance found **')
        elif keys[0] in self.__valid_classes and keys[1] == "update":
            f_w = [word.strip('"()"') for word in keys]
            valid = "{" in item
            if not valid:
                key_value = f'{keys[0]}.{f_w[2]}'
                attr_name = f_w[3]
                attr_value = f_w[4]
                obj = objects.get(key_value, None)
                if obj is None:
                    print("** no instance found **")
                    return
                if attr_name in obj.__class__.__dict__.keys():
                    valtype = type(obj.__class__.__dict__[attr_name])
                    obj.__dict__[attr_name] = valtype(attr_value)
                else:
                    obj.__dict__[attr_name] = attr_value
                models.storage.save()
                models.storage.reload()
            else:
                key_value = f'{keys[0]}.{f_w[2]}'
                obj = objects.get(key_value, None)
                if obj is None:
                    print("** no instance found **")
                    return
                open_bracket = item.find("{")
                close_bracket = item.rfind("}")
                dic = item[open_bracket:close_bracket + 1]
                vdic = eval(dic)
                for k, v in vdic.items():
                    if (k in obj.__class__.__dict__.keys() and
                            type(obj.__class__.__dict__[k]) in
                            {str, int, float}):
                        valtype = type(obj.__class__.__dict__[k])
                        obj.__dict__[k] = valtype(v)
                    else:
                        obj.__dict__[k] = v
                models.storage.save()
                models.storage.reload()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
