import json
import string
import random

def password_from_config_file(filepath: str) -> str:
    with open(filepath, 'rt') as f:
        config = f.read()
    pg = PasswordGenerator(config)
    password = pg.new()
    return password

class PasswordGenerator:

    def __init__(self, config: str):

        self.rules = json.loads(config)

        # make a string of all allowed characters
        try:
            all_allowed_characters = ''
            for key in self.rules["allowed_characters"]: #loop through each kv pair in allowed characters
                allowed_characters = ''
                for key_2 in self.rules["allowed_characters"][key]: #loop through each kv pair in groups and constants
                    chars = self.rules["allowed_characters"][key][key_2]
                    if chars == "ascii_lowercase": 
                        chars = string.ascii_lowercase
                        self.rules["allowed_characters"][key][key_2] = chars
                    elif chars == "ascii_uppercase":
                        chars = string.ascii_uppercase
                        self.rules["allowed_characters"][key][key_2] = chars
                    elif chars == "digits":
                        chars = string.digits
                        self.rules["allowed_characters"][key][key_2] = chars
                    elif chars == "ascii_letters":
                        chars = string.ascii_letters
                        self.rules["allowed_characters"][key][key_2] = chars
                    allowed_characters += chars
                all_allowed_characters += allowed_characters
            self.allowed_characters = all_allowed_characters
        except:
            pass
        
        self.violations = self.rules["violations"]
        
        #Check the length of required characters
        try:
            required_chars_rules = self.rules["required_characters"]
            req_chars_length = 0
            for req in required_chars_rules:
                req_chars_length += req[0]
        except:
            pass
        length_given = True

        # Use length if a length is specified
        try:
            self.length = self.rules["length"]
        except:
            length_given == False
            self.length = 10

        #In case the number of required chars is greater than the given length, increase the length
        if req_chars_length > self.length:
            if not length_given:
                self.length = req_chars_length
            else:
                print("Error: Invalid length requirment")
                self.length = req_chars_length   #automatically corrected to appropriate length

        pass

    '''
    new():
        Creates a new password by first gathering all required characters, then add random characters.
        Fix the password if there any violations of the given rules.
    '''
    def new(self) -> str:

        #get required chars
        required_chars = self.get_req_chars()

        #Check that req chars do not violate occurrance rule
        violations = self.rules["violations"]
        while self.check_occurrence_rule(required_chars) == False:
            required_chars = self.get_req_chars()

        #add random chars to req chars to create password
        password = ''.join(random.choice(self.allowed_characters) for _ in range(self.length - len(required_chars)))
        password += required_chars

        #fix any occurrance rule violation
        while self.check_occurrence_rule(password) == False:
            password = ''.join(random.choice(self.allowed_characters) for _ in range(self.length - len(required_chars)))
            password += required_chars
        
        #check that the refined password does not violate other rules, if so just shuffle the string
        while self.check_consecutive_rule(password) == False or self.check_sequential_rule(password) == False or self.check_verboten_rule(password) == False:
            password = ''.join(random.sample(password,len(password)))
        
        print(password)
        return password

    '''
    allowed(password):
        This method returns true if the password requirements are met and there are no violations
    '''
    def allowed(self, password: str) -> bool:
        password_allowed = True

        #check if characters are allowed
        for ch in password:
            if ch not in self.allowed_characters:
                password_allowed = False
                break
        
        #check length
        if len(password) < self.length:
            password_allowed = False
        
        #check if required characters are present
        required_characters = self.rules["required_characters"]
        for req in required_characters:
            if password_allowed:
                total_found = 0
                for ch in password:
                    if ch in self.rules["allowed_characters"][req[1]+"s"][req[2]]:
                        total_found +=1
                if total_found < req[0]:
                    password_allowed = False
                    print(" REQUIRED CHARACTERS FAILED")
                    break
        
        #check violations

        if self.check_consecutive_rule(password) == False:
            print(" CONSECUTIVE RULE FAILED")
            password_allowed = False

        if self.check_occurrence_rule(password) == False:
            print(" OCCURRANCE RULE FAILED")
            password_allowed = False

        if self.check_sequential_rule(password) == False:
            print(" SEQUENTIAL RULE FAILED WITH:")
            password_allowed = False

        if self.check_verboten_rule(password) == False:
            print(" VERBOTEN RULE FAILED")
            password_allowed = False

        return password_allowed

    '''
    check_consecutive_rule(password):
        This method returns false if there is a violation of the "consecutive" rule.
    '''
    def check_consecutive_rule(self, password) -> bool:
        passed = True
        try:
            consecutive_limit = self.violations["consecutive"]
            consecutives_found = 1
            for i in range(len(password) -1):
                if password[i] == password[i+1]:
                    consecutives_found +=1
            if consecutives_found >= consecutive_limit:
                passed = False
        except:
            pass
        return passed

    '''
    check_occurrence_rule(password):
        This method returns false if there is a violation of the "occurrence" rule
    '''
    def check_occurrence_rule(self, password) -> bool:
        passed = True
        try:
            occurrence_limit = self.violations["occurrence"]
            for ch in password:
                if password.count(ch) >= occurrence_limit:
                    passed= False
                    break
        except:
            pass
        return passed
    '''
    check_sequential_rule(password):
        This method returns false if there is a violation of the "sequential" rule
    '''
    def check_sequential_rule(self, password) -> bool:
        passed = True
        try:
            sequential_rule = self.violations["sequential"]
            for rule in sequential_rule:
                chars = self.rules["allowed_characters"][rule[1]+"s"][rule[2]]
                seq_limit = rule[0]
                j = seq_limit - 1
                for i in range(len(chars)-j):
                    sub_str = chars[i:i+seq_limit]
                    sub_str_rev = sub_str[::-1]
                    if sub_str in password or sub_str_rev in password:
                        passed = False
                        break 
        except:
            pass
        return passed

    '''
    check_verboten_rule(password):
        This method returns false if there is a violation of the "verboten" rule
    '''
    def check_verboten_rule(self, password) -> bool:
        passed = True
        try:
            verboten = self.violations["verboten"]
            for sub_str in verboten:
                if sub_str in password:
                    passed = False
                    break
        except:
            pass
        return passed
    '''
    get_req_chars():
        This method returns a set of randomly chosen, required characters
    '''
    def get_req_chars(self) -> str:
        required_chars_rules = self.rules["required_characters"]
        required_chars = ''
        for req in required_chars_rules:
            chars = self.rules["allowed_characters"][req[1]+"s"][req[2]]
            sub_str = ''.join(random.choice(chars) for _ in range(req[0]))
            required_chars += sub_str
        return required_chars



