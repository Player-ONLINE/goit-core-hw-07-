from main_task_ import AddressBook, Record

def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0], parts[1:]

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            if len(args) < 2:
                print("Usage: add [name] [phone]")
            else:
                name, phone = args[0], args[1]
                record = book.find(name)
                if not record:
                    record = Record(name)
                    book.add_record(record)
                record.add_phone(phone)
                print(f"Contact {name} updated.")

        elif command == "change":
            if len(args) < 3:
                print("Usage: change [name] [old_phone] [new_phone]")
            else:
                name, old_phone, new_phone = args
                record = book.find(name)
                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print(f"Phone number updated for {name}.")
                    except ValueError as e:
                        print(e)
                else:
                    print(f"Contact {name} not found.")

        elif command == "phone":
            if len(args) < 1:
                print("Usage: phone [name]")
            else:
                record = book.find(args[0])
                if record:
                    print(f"{record.name}: {', '.join(p.value for p in record.phones)}")
                else:
                    print(f"Contact {args[0]} not found.")

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            if len(args) < 2:
                print("Usage: add-birthday [name] [DD.MM.YYYY]")
            else:
                name, birthday = args
                record = book.find(name)
                if record:
                    try:
                        record.add_birthday(birthday)
                        print(f"Birthday added for {name}.")
                    except ValueError as e:
                        print(e)
                else:
                    print(f"Contact {name} not found.")

        elif command == "show-birthday":
            if len(args) < 1:
                print("Usage: show-birthday [name]")
            else:
                record = book.find(args[0])
                if record and record.birthday:
                    print(f"{record.name}'s birthday: {record.birthday}")
                else:
                    print(f"Birthday not found for {args[0]}.")

        elif command == "birthdays":
            upcoming = book.get_upcoming_birthdays()
            if upcoming:
                print("Upcoming birthdays:")
                for b in upcoming:
                    print(f"{b['name']} - {b['congratulation_date']}")
            else:
                print("No upcoming birthdays.")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
