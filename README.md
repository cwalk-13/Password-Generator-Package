# Password-Generator-Package
A python package that generates a password given specific requirements outlined in a json file.

## Installation Steps:
1. Clone the repository
2. Move into the "Password-Generator-Package" directory
3. With Pyhton installed, run the command 
```bash
pip install . 
```
4. If this does not work, the alternative command is 
```bash
pip install password_gen_cw
```
5. Close and reopen your environment before tessting

## Testing and Use: 
* Once the package is installed, try running the "test.py" and "test_strong.py" files located in the "Password-Generator-Package"
  * Notice the tests' output in the console.
* If you are outside of the package directory you can import the module like so:
```python
from password_gen_cw import PasswordGenerator

with open('path/to/config.json', 'rt') as f:
    config = f.read()

pgen = PasswordGenerator(config)

new_password = pgen.new()
```
Or
``` python
import password_gen_cw as pg

new_password = pg.password_from_config_file('path/to/config.json')
```
* I named the package "password_gen_cw" because I had problems trying to use "password_gen", there may already be a public package that uses that name.
