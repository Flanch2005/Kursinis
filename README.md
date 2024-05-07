# Birthday reminder

The program is a simple GUI application that assists in tracking your friends and siblings birthdays. In the program, you can create multiple accounts to create a separation between birthdays if several people use the same program at once.

It is written in Python and uses the `tkinter` and its extensions `customtkinter` libraries to create the GUI.

To run the program, you need Python 3.11 or later. You can open the program by using either `Visual Studio Code` or `PyCharm`, by using their inbuilt run operations. Alternatively, you have the option to download the compiled program from `Tags - 1.0`.

## Analysis of the Implementations


The program allows users to: 

- **Create Accounts**: Each user can create a personal account to manage their own set of birthdays.
- **Save Birthdays**: Once logged in, users can add and save birthdays to their account.
- **View Birthdays**: Users can view all saved birthdays in a list within the main window.
- **Edit Birthdays**: Users have the option to edit or delete any saved birthday information.
- **Search Functionality**: There is a search bar to quickly find a specific birthday by name.
- **Notifications**: The program can be set to give notifications as reminders for upcoming birthdays, using the `notify-py` module for implementing these notifications.
- **Minimize to Tray**: The program can be minimized to the system tray for convenience.

`customtkinter` is used in the application to create a more visually appealing and modern user interface. Here is an example of how `customtkinter` is utilized to create the main login window in the application:

```python
 main_screen = customtkinter.CTk()
    main_screen.minsize(width=300, height=200)
    main_screen.maxsize(width=300, height=200)
    main_screen.title("Account Login")

    _label = customtkinter.CTkLabel(master=main_screen, text="Login Or Create new user", font=("Calibri", 20, "bold"))
    _space1 = customtkinter.CTkLabel(master=main_screen, text="")
    _button = customtkinter.CTkButton(master=main_screen, text="Login", height=40, width=100, corner_radius=50,
                                      command=login)
    _space2 = customtkinter.CTkLabel(master=main_screen, text="")
    _button2 = customtkinter.CTkButton(master=main_screen, text="Create new user", height=40, width=100,
                                       corner_radius=50, command=register) 
```

The example of using the `notify-py` module in the application
```python
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


        notification = Notify()
        notification.title = "Birthday reminder"
        notification.message = f"Wish a happy birthday to: {full_name} \n Contact info: {contact_info}"
        notification.send()
```
When adding new birthdays, the application saves them in a specific format
```python
class Contact(Person):
    def __init__(self, name, last_name, birthday, email, phone_number):
        import re
        pattern = re.compile(r'\s+')
        name = re.sub(pattern, '', name)
        last_name = re.sub(pattern, '', last_name)
        birthday = re.sub(pattern, '', birthday)
        email = re.sub(pattern, '', email)
        phone_number = re.sub(pattern, '', phone_number)

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
```
