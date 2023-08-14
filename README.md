# Description
This is the first section of the AirBnB clone for the ALX Software Engineering program. In this section we made a command interpreter CLI console using the `cmd` python module.

# Details
The project is intended to make a command interpreter in Python using CLI. The commands accounted for are:
* `EOF`: Causing the end of file condition. Used as `EOF``
* `quit`: Closing the console. e.g. `quit`
* `create`: To create an instance of a class returning the ID of that instance e.g. `create \<classname\>`
* `show`: To show the string representation of an instance using its classname and ID e.g. `show \<classname\> \<id\>`
* `destroy`: To destroy an instance using its classname and ID e.g. `destroy \<classname\> \<id\>`
* `all`: To print all instances of a class or all classes e.g. `all \<classname\>` or `all`
* `update`: To update an instance using its classname and ID `update \<class name\> \<id\> \<attribute name\> "\<attribute value\>"`
* `count`: To retrieve the number of instances of a class. `count \<class name\>`

# Notes
The commands can be called in the format `cmd \<args\>` or `classname.cmd(args)`
The console can be called in interactive and non interactive mode

