from classes.personClass import Person


class Contact(Person):
    def __init__(self, name, last_name, birthday, email, phone_number):
        import re
        pattern = re.compile(r'\s+')
        name = re.sub(pattern, '', name)
        last_name = re.sub(pattern, '', last_name)
        birthday = re.sub(pattern, '', birthday)
        email = re.sub(pattern, '', email)
        phone_number = re.sub(pattern, '', phone_number)

        # Paveldejimas
        super().__init__(name, last_name, birthday)

        self._email = email
        self._phone_number = phone_number

    def get_contact_info(self):
        return {"email": self._email, "number": self._phone_number}

    def send_reminder(self):
        from classes.popUpReminder import PopUpReminder
        reminder = PopUpReminder()
        reminder.send_reminder(self)

    def get_contact_formated(self):
        return self._name + " " + self._last_name + " " + self._birthday + " " + self._email + " " + self._phone_number
