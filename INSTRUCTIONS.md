# Configurable Password Generator

## Overview

Being able to generate random passwords is useful, but different services
have different requirements for valid passwords.

The object of this exercise is to create a Python package that allows the user
to generate random passwords that meet requirements that the user defines in a
configuration JSON.

For the purpose of this exercise, four requirements (or requirement types) may 
be imposed:

* **Length**: The length requirement of the password.

* **Allowed Characters:** A set of characters that may be used for password
  generation.

* **Required Characters:** Requirements that the final password must include *n*
  instances from some set or sets of characters. For example, the user could 
  specify that a password must include 2 capital letters and 3 "special characters"
  (however the user defines "special characters")

* **Violations:** Conditions which cannot exist in the password. For example, the user
  could specify that the password cannot contain 2 repeated characters in a row,
  and may not contain the same character 3 or more times.

Two example configuration files are provided. Your package *must* support enforcement
of all the requirements defined in the `config.json` file. Importantly, your
implementation should plan to be *extended* so that support all of the requirements
in the `config_strong.json` file can be implemented in a straightfoward way. If
you wish to fully implement all the requirements of the 
`config_strong.json`, feel free to do so.

Further notes on the `config.json` file are found in a section below, titled
"Notes on config.json".

For this exercise, you may consult any online resources that you like, but the
solution should be your own. Evidence that a significant amount of code has been
lifted or only minorly adapted from an outside source will reflect negatively
on the assessment of your work.


## Environment

* Python 3.7.9
* Please use only the Python standard library for creating the solution.
* The `setuptools` package for packaging

## Packaging

Your code should be organized as a package that uses `setuptools` to create
distributions. Please use the older `setup.py` method, rather than creating a
configuration file. For the purpose of this excercise, the package name should be
`password_gen`

If you're not familiar with this type of package layout, here is the general
directory structure that should be used. The top-level folder has been named
`password-generator`, but could be named anything:

```
password-generator/
    setup.py        # This script runs the `setuptools.setup()` function
    password_gen/
        ...         # Your source code goes here
```

And for more direction, see the documentation for `setuptools`.


## Interface

Your package should have one user-facing class named `PasswordGenerator`.

Here is a basic interface for `PasswordGenerator`:

```python
class PasswordGenerator:

    def __init__(self, config: str):
        pass

    def new(self) -> str:
        pass

    def allowed(self, password: str) -> bool:
        pass
```

In the `__init__` method's signature, `config` is a JSON-formatted string. The 
`new` method should return a password as a `str`. The `allowed` accepts a
password string as an argument and returns a `bool` indicating whether or not
that password meets the config requirements.

Your package should also contain a convenience function named
`password_from_config_file` with a signature:

```python

def password_from_config_file(filepath: str) -> str:
    pass

```

Which accepts a `str` that gives the path to a config JSON and returns a single
password which meets the requirements specified in that config file.


## Expected Functionality

There are a couple of use cases. Your package should support the first and may
optionally support the second:

### Use Case #1: As a library whose objects can be imported and used in other code.

Your package should support the following library uses:

```python
from password_gen import PasswordGenerator

with open('path/to/config.json', 'rt') as f:
    config = f.read()

pgen = PasswordGenerator(config)

new_password = pgen.new()
```

And also this:


```python
from password_gen import password_from_config_file

new_password = password_from_config_file('path/to/config.json')
```

### Optional Use Case #2: As a command line tool

If you choose, your package can the following command-line use:

The command

```bash
python -m password_gen path/to/config.json
```

Should print out a new password to stdout which meets the requirements specified
in the `config.json`.


## Tests

Two testing scripts have been provided, `test.py` and `test_strong.py`, and they
can be used to test passwords from the two config files that are provided. The
testing scripts expect to be located in the same directory as the config files
and run from within that directory. These scripts also expect that you have
named your package `password_gen`, have installed it in your working environment,
and have followed the interface described above.

These testing scripts provide some basic pass/fail coverage for the core 
functionalities of the excercise, but edge cases and full-coverage testing are
up to you if you have time!


## Notes on config.json

A part of this exercise challenges your ability to infer design, so not everything
about the config.json file format is explained in these instructions.

Take note that the basic `config.json` example doesn't make use of all the structural
elements shown in the breakdown below. (The `config_strong.json` does, however.) 
An initial implementation could simply focus on the elements that are present in
that basic config file. 

Here is a breakdown of the full structure of the JSON object:

```json
{
    "length": int,

    "allowed_characters": {
        "groups": {
            string: string,
            string: string,
            etc...
        },
        "constants": {
            string: string,
            string: string,
            etc...
        }
    },

    "required_characters" : [
        [int, string, string],
        [int, string, string],
        etc...
    ],

    "violations" : {
        "consecutive": int,
        "occurrence": int,
        "sequential": [
            [int, string, string],
            [int, string, string],
            etc...
        ],
        "verboten": [
            string,
            string,
            etc...
        ]
    }
}
```

Here are a few more notes on some of the subsections:

### `length`

This should be optional, and a default value should be provided by the 
application if this is missing from the config.

### `allowed_characters`

This section is a mapping that can have two keys:  `"groups"` and `"constants"`.

For an explanation of the values found in the `"constants"` section, see:
[Python - string - String constants](https://docs.python.org/3/library/string.html#string-constants)


### `required_characters` and `violations`

The `[int, string, string]` pattern is always `[count, group_type, group]`. The
`group_type` will always be either `group` or `constant`, with the same meanings
of those terms as is found in the `allowed_characters` section.

If some element of the `violations` section is not provided in the config JSON,
or if it is defined as `null`, that element has no rule to enforce.


### Here's an example of a `violations` section.

In plain English, here are some example violation requirements. 

    A password may not contain:
    * A single character repeated 2 or more times consecutively
    * A single character that occurs 4 or more times
    * A series of sequential numbers (0-9) that is 3 or more characters long and
      was provided in the "groups" mapping of the "allowed_characters" requirement.
         ("123" is wrong, "765" is wrong, "465" is OK)
    * The substring "password"

In the config file, these would be defined:

```json
{
    ...,
    "violations" :{
        "consecutive": 2,
        "occurrence":4,
        "sequential": [
            [3, "group", "numbers"]
        ],
        "verboten":[
            "password"
        ]
    }
}
```
