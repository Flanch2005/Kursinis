class Person:
    def __init__(self, name, last_name, birthday):
        self._name = name
        self._last_name = last_name
        self._birthday = birthday
        self._birthdayFormated = self.format_birthday(birthday)

    def get_full_name(self):
        return {"name": self._name, "last_name": self._last_name}

    def get_birthday(self):
        return self._birthday

    def format_birthday(self, date):
        import datetime
        string = date.split("-")
        year = int(string[0])
        month = int(string[1])
        day = int(string[2])
        return datetime.datetime(year, month, day)

    def get_formated_date(self):
        return self._birthdayFormated
