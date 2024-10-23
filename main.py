from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return re.fullmatch(r"\d{10}", phone)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        del self.data[name]

# ----------------- Логіка для команд ----------------- #

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return f"Error: Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Error: Please provide all required arguments."
    return inner

@input_error
def add_contact(args, address_book):
    name, phone = args
    if address_book.find(name):
        return f"Contact {name} already exists."
    new_record = Record(name)
    new_record.add_phone(phone)
    address_book.add_record(new_record)
    return f"Contact {name} added."

@input_error
def change_contact(args, address_book):
    name,new_phone = args
    record = address_book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return f"Contact {name} updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return f"{name}: {"; ".join(p.value for p in record.phones)}"
    return "Contact not found."

@input_error
def show_all(address_book):
    if address_book.data:
        return "\n" .join([str(record) for record in address_book.data.values()])
    else:
        return "No contacts available."
    
# ----------------- Основна програма ----------------- #

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, address_book))
        elif command == "change":
            print(change_contact(args, address_book))
        elif command == "phone":
            print(show_phone(args, address_book))
        elif command == "all":
            print(show_all(address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()