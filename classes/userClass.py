from classes.contactClass import Contact


class User:
    def __init__(self, username):
        self._username = username
        self._contacts = self.read_birthdays()

    def get_username(self):
        return self._username

    def get_contacts(self):
        return self._contacts

    def read_birthdays(self):
        import json
        import os
        current_dir = os.path.expanduser("~")

        # For distribution build
        database_path = os.path.join(current_dir, "_internal", "database")

        if not os.path.exists(database_path):
            # For IDE run
            database_path = os.path.join(current_dir, "database")

        if not os.path.isdir(database_path):
            os.makedirs(database_path)

        f = open(os.path.join(database_path, self.get_username() + ".json"))
        data = json.load(f)
        contacts = list()
        for i in data['birthdays']:
            _contact = Contact(i['name'], i['last_name'], i['birthday'], i['email'], i['number'])
            contacts.append(_contact)
        f.close()
        return contacts

    def add_contact(self, name, last_name, email, number, birthday):
        dictionary = {
            "name": name,
            "last_name": last_name,
            "email": email,
            "number": number,
            "birthday": birthday
        }

        import json
        import os


        current_dir = os.path.expanduser("~")

        # For distribution build
        database_path = os.path.join(current_dir, "_internal", "database")

        if not os.path.exists(database_path):
            # For IDE run
            database_path = os.path.join(current_dir, "database")

        if not os.path.isdir(database_path):
            os.makedirs(database_path)

        with open(os.path.join(database_path, self._username + ".json"), 'r+') as file:
            data = json.load(file)
            data["birthdays"].append(dictionary)
            file.seek(0)
            json.dump(data, file, indent=4)
        contact = Contact(name, last_name, birthday, email, number)
        self._contacts.append(contact)
        self.check_if_birthday(contact)

    def check_if_birthday(self, contact):
        from datetime import date
        string = contact.get_birthday().split("-")
        month = int(string[1])
        day = int(string[2])
        today = date.today()
        if month == today.month and day == today.day:
            if not isinstance(contact, Contact):
                raise TypeError("Expected a string object.")
            contact.send_reminder()

    def find_contact(self, contact_data):
        if not isinstance(contact_data, str):
            raise TypeError("Expected a string object.")
        string = contact_data.split()
        for contact in self.get_contacts():
            if not isinstance(contact, Contact):
                raise TypeError("Expected a Contact object.")

            if contact_data == contact.get_contact_formated():
                return contact
        return None

    def delete_contact(self, contact_data):
        contact = self.find_contact(contact_data)

        self._contacts.remove(contact)
        import json
        import os

        current_dir = os.path.expanduser("~")

        # For distribution build
        database_path = os.path.join(current_dir, "_internal", "database")

        if not os.path.exists(database_path):
            # For IDE run
            database_path = os.path.join(current_dir, "database")

        if not os.path.isdir(database_path):
            os.makedirs(database_path)

        dictionary = {"birthdays": []}
        json_object = json.dumps(dictionary)
        json_file_path = os.path.join(database_path, self._username + ".json")
        json_object = json.dumps(dictionary)
        with open(json_file_path, "w") as outfile:
            outfile.write(json_object)

        with open(os.path.join(database_path, self._username + ".json"), 'r+') as file:
            data = json.load(file)
            for contact in self._contacts:
                if not isinstance(contact, Contact):
                    raise TypeError("Expected a Contact object.")
                full_name = contact.get_full_name()
                name = full_name["name"]
                last_name = full_name["last_name"]
                contact_info = contact.get_contact_info()
                email = contact_info["email"]
                number = contact_info["number"]
                dictionary = {
                    "name": name,
                    "last_name": last_name,
                    "email": email,
                    "number": number,
                    "birthday": contact.get_birthday()
                }
                data["birthdays"].append(dictionary)

            file.seek(0)
            json.dump(data, file, indent=4)
