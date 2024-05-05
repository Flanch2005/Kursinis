from notifypy import Notify

from classes.contactClass import Contact
from classes.reminderClass import Reminder


# Paveldi is abstraktaus metodo
class PopUpReminder(Reminder):
    def send_reminder(self, contact):

        if not isinstance(contact, Contact):
            raise TypeError("Expected a Contact object.")

        data = contact.get_full_name()
        full_name = data["name"] + " " + data["last_name"]

        data = contact.get_contact_info()

        if data is None:
            contact_info = "None"
        else:
            contact_info = data["email"] + " " + data["number"]

        # notification = plyer.platforms.win.notification.instance() notification.notify("Birthday reminder",
        # f"Wish a happy birthday to: {full_name} \n Contact info: {contact_info}")
        notification = Notify()
        notification.title = "Birthday reminder"
        notification.message = f"Wish a happy birthday to: {full_name} \n Contact info: {contact_info}"
        notification.send()
