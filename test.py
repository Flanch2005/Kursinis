import unittest

from classes.contactClass import Contact
from classes.personClass import Person


class ContactTest(unittest.TestCase):
    def __init__(self, method_name="runTest"):
        super().__init__(method_name)

        self.contact = Contact("Test", "Test", "2023-01-01", "example@example.com", "+0")

    def test_format(self):
        self.assertEqual("Test Test 2023-01-01 example@example.com +0", self.contact.get_contact_formated())

    def test_contact_info(self):
        self.assertDictEqual({"email": "example@example.com", "number": "+0"}, self.contact.get_contact_info())


class PersonTest(unittest.TestCase):
    def __init__(self, method_name="runTest"):
        super().__init__(method_name)

        self.person = Person("Test", "Test", "2023-01-01")

    def test_full_name(self):
        self.assertDictEqual({"name": "Test", "last_name": "Test"}, self.person.get_full_name())

    def test_birthday(self):
        self.assertEqual("2023-01-01", self.person.get_birthday())


if __name__ == "__main__":
    unittest.main()

