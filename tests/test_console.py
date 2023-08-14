#!/usr/bin/python3
""" unittest cases for the console """

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import json
import re
import cmd
import models
from models import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):
    """ tst class """

    @classmethod
    def setUpClass(cls):
        """ setup class """
        cls.hbnb = HBNBCommand()
        cls.mock_stdout = StringIO()

    def setUp(self):
        """ setup self """
        models.storage = FileStorage()
        self.hbnb.stdout = self.mock_stdout

    def tearDown(self):
        """ another test case """
        models.storage._FileStorage__objects = {}
        self.mock_stdout.seek(0)
        self.mock_stdout.truncate()

    def test_quit(self):
        """ test for quit """
        self.assertTrue(self.hbnb.do_quit(''))
    
    def test_EOF(self):
        """ checking EOF """
        self.assertTrue(self.hbnb.do_EOF(''))
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_emptyline(self, mock_stdout):
        """ test case """
        self.hbnb.emptyline()
        self.assertEqual(mock_stdout.getvalue(), '')


    def test_show_valid_input(self):
        """ tset case """
        test_user = User()
        test_user.save()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.do_show(f"User {test_user.id}")
            self.assertIn(str(test_user), mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_invalid_class(self, mock_stdout):
        """ no so good with test cases """
        self.hbnb.do_show('InvalidClass 123')
        self.assertEqual(mock_stdout.getvalue(), "** class doesn't exist **\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_show_missing_id(self, mock_stdout):
        """ for the Lord is Good """
        self.hbnb.do_show('User')
        self.assertEqual(mock_stdout.getvalue(), "** instance id missing **\n")

    def test_destroy_valid_input(self):
        """ test for destroy """
        test_user = User()
        test_user.save()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.do_destroy(f"User {test_user.id}")
            self.assertEqual(mock_stdout.getvalue(), "")
        self.assertNotIn(test_user.id, models.storage.all())

    @patch('sys.stdout', new_callable=StringIO)
    def test_destroy_invalid_class(self, mock_stdout):
        """ test on destroy method """
        self.hbnb.do_destroy('InvalidClass 123')
        self.assertEqual(mock_stdout.getvalue(), "** class doesn't exist **\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_destroy_missing_id(self, mock_stdout):
        """ test for missing id """
        self.hbnb.do_destroy('User')
        self.assertEqual(mock_stdout.getvalue(), "** instance id missing **\n")


    @patch('sys.stdout', new_callable=StringIO)
    def test_all_invalid_class(self, mock_stdout):
        """ test for invalid class """
        self.hbnb.do_all('InvalidClass')
        self.assertEqual(mock_stdout.getvalue(), "** class doesn't exist **\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_invalid_class(self, mock_stdout):
        """ test for valid classes """
        self.hbnb.do_update('InvalidClass 123 name "New Name"')
        self.assertEqual(mock_stdout.getvalue(), "** class doesn't exist **\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_missing_id(self, mock_stdout):
        """ test for missing id """
        self.hbnb.do_update('User')
        self.assertEqual(mock_stdout.getvalue(), "** instance id missing **\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_missing_attr_name(self, mock_stdout):
        """ test for missing attribute """
        self.hbnb.do_update('User 12345')
        self.assertEqual(mock_stdout.getvalue(), "** attribute name missing **\n")

    @patch('sys.stdout', new_callable=StringIO)
    def test_update_missing_value(self, mock_stdout):
        """ test for missing id """
        self.hbnb.do_update('User 12345 name')
        self.assertEqual(mock_stdout.getvalue(), "** value missing **\n")

    def test_default_all_command(self):
        """ test for the default cases """
        with patch.object(models.storage, 'all') as mock_all:
            mock_all.return_value = {'User.123': User(), 'Place.456': Place()}
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.hbnb.default('all User')
                output = mock_stdout.getvalue().strip()
                self.assertNotIn("Place.456", output)

    def test_default_count_command(self):
        """ test on the count cases """
        with patch.object(models.storage, 'all') as mock_all:
            mock_all.return_value = {'User.123': User(), 'User.456': User()}
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.hbnb.default('count User')


    def test_default_show_command_invalid(self):
        """ test on the show command """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.default('show InvalidClass 123')
            self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    def test_default_destroy_command_valid(self):
        """ test on the destroy cases """
        test_user = User()
        test_user.save()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.default('destroy User ' + test_user.id)

    def test_default_destroy_command_invalid(self):
        """ test on the destroy cases """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.default('destroy InvalidClass 123')
            self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

    def test_default_update_command_valid(self):
        """ test ob update command valid """
        test_user = User()
        test_user.save()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.default('update User ' + test_user.id + ' name "New Name"')


    def test_default_update_command_invalid(self):
        """ test on invalid command """
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.hbnb.default('update InvalidClass 123 name "New Name"')
            self.assertEqual(mock_stdout.getvalue().strip(), "** class doesn't exist **")

if __name__ == '__main__':
    unittest.main()
