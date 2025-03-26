from collections import UserDict
import datetime
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
    
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Phone number not found.")
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "No phones"
        birthday = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact: {self.name.value}, Phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

    def get_upcoming_birthdays(self):
        today = datetime.date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue   

            bday = datetime.datetime.strptime(record.birthday.value, "%d.%m.%Y").date().replace(year=today.year)

            if bday < today:
                bday = bday.replace(year=today.year + 1)

            days_until_bday = (bday - today).days

            if 0 < days_until_bday <= 7:
                if bday.weekday() in {5, 6}:  
                    bday += datetime.timedelta(days=(7 - bday.weekday()))   

                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": bday.strftime("%d.%m.%Y")})

        return upcoming_birthdays

# Тестування

book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("28.03.2000")
book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("30.03.1995")
book.add_record(jane_record)

print("Всі контакти:")
print(book)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print("\n Відредагований контакт Джона:")
print(john)

found_phone = john.find_phone("5555555555")
print(f"\n Знайдений телефон у Джона: {found_phone}")

book.delete("Jane")
print("\n Видалили Джейн. Оновлений список контактів:")
print(book)

print("\nБлизькі дні народження:")
print(book.get_upcoming_birthdays())