import os
from datetime import datetime
from abc import ABC

# =============== VARIABLES ===============
users:list["User"] = []
notes:list["Note"] = []
current_user = None

# =============== MODELS ===============
class User(ABC):
    def __init__(self, uname, pw, fname):
        self.fname = fname
        self.uname = uname
        self.pw = pw

    def __repr__(self):
        return f"{self.fname} - {self.uname}"

# Def user
users.append(User("cuckoodile", "pass", "Renekton"))

class Note(ABC):
    def __init__(self, title, description, user):
        self.title = title
        self.description = description
        self.user = user
        self._created_at = None
        self._updated_at = None

        self.created_at = None
        self.updated_at = None

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, _):
        self._created_at = datetime.now()
        
    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, _):
        self._updated_at = datetime.now()

    def __repr__(self):
        return f"{self.title} - {self._created_at}"

# =============== HELPER FUNCTIONS ===============
def prompt(message: str, type_cast = int):
    os.system('cls')
    return type_cast(input(message))

def my_print(message:str):
    os.system('cls')
    print(message)

def get_user(un, users) -> User | None:
    for user in users:
        if un in user.uname:
            return user

    print(f"User {un} not found!")
    return None

# =============== CONTROLLER ===============
def login():
    un = prompt("Username: ", str)
    pw = prompt("Password: ", str)
    
    if not un.strip() or not pw.strip():
        print("Username and Password cannot be empty!")

    if users:
        for user in users:
            print(type(user))
            if un == user.uname and pw == user.pw:
                return user

    print("Invalid Credentials!")
    return None

def register() -> User | None:
    fn = prompt("Full Name: ", str)
    un = prompt("Username: ", str)
    pw = prompt("Password: ", str)
    cpw = prompt("Confirm Password: ", str)

    if pw != cpw:
        print("Password and Confirm Password does not match")
        return None

    us = User(un, pw, fn)
    users.append(us)
    return us

def list_notes():
    for i, note in enumerate(notes):
        if current_user == note.user:
            my_print(f"[{i}] {note}")

def create_note():
    title = prompt("Title: ", str)
    description = prompt("Description: ", str)

    note = Note(title, description, current_user)
    notes.append(note)
    return note

def update_note():
    pass

def delete_note():
    pass

# =============== MAIN FLOW ===============
while True:
    if current_user is None:
        # Main Menu
        print("Welcome to Frieren's Notepad")
        action = int(input("""Select an action number:
        [0] EXIT
        [1] LOGIN
        [2] REGISTER
        """))
    
        match(action):
            case 0:
                my_print("Thank you!")
                break
            case 1:
                current_user = login()
            case 2:
                current_user = register()
    else:
        # User's Menu
        print(f"Hello {current_user.uname}")
        action = int(input("""
        [0] LOGOUT
        [1] LIST NOTES
        [2] CREATE NOTE
        [3] UPDATE NOTE
        [4] DELETE NOTE
        """))

        match(action):
            case 0:
                print(f"User {current_user.uname} is logged out")
                current_user = None
            case 1:
                list_notes()
            case 2:
                create_note()
            case 3:
                update_note()
            case 4:
                delete_note()