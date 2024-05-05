import datetime
import re
import threading
import time
from datetime import date
from tkinter import *

import customtkinter
import pystray
import schedule
from CTkListbox import *
from PIL import Image, ImageDraw

from classes.contactClass import Contact
from classes.userClass import User

current_user = None
global birthday_screen
global my_frame
current_day = datetime.datetime.now().date()
global run_scheduler
global current_window


def create_icon():
    image = Image.new("RGB", (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill=(0, 0, 0))
    return image


tray_icon = pystray.Icon("Birthday Reminder", icon=create_icon(), title="Birthday Reminder")


def gather_birthdays():
    user = get_user()
    contacts = user.get_contacts()
    birthdays = list()
    for contact in contacts:
        if not isinstance(contact, Contact):
            raise TypeError("Expected a Contact object.")
        string = contact.get_birthday().split("-")
        month = int(string[1])
        day = int(string[2])
        today = date.today()
        if month == today.month and day == today.day:
            birthdays.append(contact)
    return birthdays


def check_birthdays():
    birthdays = gather_birthdays()
    send_notifications(birthdays)


def check_date():
    global current_day
    if current_day < datetime.datetime.now().date():
        current_day = datetime.datetime.now().date()
        check_birthdays()


def thread_task():
    global run_scheduler
    schedule.every().hour.do(check_date)
    while run_scheduler:
        schedule.run_pending()
        time.sleep(1)


def send_notifications(contacts):
    for contact in contacts:
        if not isinstance(contact, Contact):
            raise TypeError("Expected a Contact object.")
        contact.send_reminder()


def get_user():
    global current_user
    return current_user


def logout_user():
    global current_user
    global run_scheduler
    current_user = None
    run_scheduler = False
    t1.join()
    global birthday_screen
    birthday_screen.destroy()
    main_account_screen()


def check_exists(input):
    import os
    current_dir = os.path.expanduser("~")

    # For distribution build
    database_path = os.path.join(current_dir, "_internal", "database")

    if not os.path.exists(database_path):
        # For IDE run
        database_path = os.path.join(current_dir, "database")

    if not os.path.isdir(database_path):
        os.makedirs(database_path)

    for name in os.listdir(database_path):
        with open(os.path.join(database_path, name)) as f:
            if input + ".json" == name:
                return True

    return False


def main_account_screen():
    global main_screen
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

    _label.pack()
    _space1.pack()
    _button.pack()
    _space2.pack()
    _button2.pack()
    global current_window
    current_window = main_screen
    main_screen.mainloop()


def birthday_app():
    global birthday_screen
    global run_scheduler
    run_scheduler = True

    global current_window

    main_screen.destroy()
    birthday_screen = customtkinter.CTk()
    birthday_screen.minsize(width=450, height=500)
    birthday_screen.title("Birthday App")
    current_window = birthday_screen
    logout_button = customtkinter.CTkButton(birthday_screen, text="Logout", command=logout_user)
    logout_button.pack()

    # minimize_button = customtkinter.CTkButton(birthday_screen, text="Minimize", command=minimize_to_tray)
    # minimize_button.pack()

    new_button = customtkinter.CTkButton(birthday_screen, text="Add new Birthday", command=add_contact)
    new_button.pack()

    delete_button = customtkinter.CTkButton(birthday_screen, text="Delete Selected", command=delete_contact)
    delete_button.pack()

    customtkinter.CTkLabel(birthday_screen, text="").pack()

    search_bar_type = StringVar()
    global search_bar
    search_bar = customtkinter.CTkEntry(birthday_screen, textvariable=search_bar_type)
    search_button = customtkinter.CTkButton(birthday_screen, text="Search", command=searched_contacts)

    search_bar.bind("<Return>", lambda event: searched_contacts())
    search_bar.pack()
    search_button.pack()

    sync_contacts(get_user().get_contacts())

    global t1
    t1 = threading.Thread(None, target=thread_task)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(None, target=check_birthdays)
    t2.deaemon = True
    t2.start()

    birthday_screen.protocol("WM_DELETE_WINDOW", minimize_to_tray)
    birthday_screen.mainloop()


def minimize_to_tray():
    birthday_screen.withdraw()


def restore_from_tray():
    birthday_screen.deiconify()


def close_application():
    tray_icon.stop()
    global run_scheduler
    run_scheduler = False
    t1.join()
    global current_window
    current_window.destroy()


def searched_contacts():
    val = search_bar.get()
    search_bar.delete(0, END)
    if val == '':
        return
    else:
        global search_screen
        search_screen = customtkinter.CTkToplevel(birthday_screen)
        search_screen.title("Searched contacts")
        search_screen.minsize(width=500, height=500)
        search_screen.attributes('-topmost', True)

        user = get_user()
        contacts = user.get_contacts()
        data = []
        for contact in contacts:
            if not isinstance(contact, Contact):
                raise TypeError("Expected a Contact object.")
            if str(val).lower() in str(contact.get_contact_formated()).lower():
                data.append(contact)

    list = CTkListbox(search_screen)
    list.pack(fill="both", expand=True, padx=10, pady=10)
    i = 0
    for contact in data:
        if not isinstance(contact, Contact):
            raise TypeError("Expected a Contact object.")
        text = contact.get_contact_formated()
        if data is None:
            raise TypeError("Expected data in user")
        list.insert(i, text)
        i = i + 1


def sync_contacts(contacts):
    global birthday_screen
    global my_frame
    my_frame = CTkListbox(birthday_screen)
    my_frame.pack(fill="both", expand=True, padx=10, pady=10)
    i = 0
    for contact in contacts:
        if not isinstance(contact, Contact):
            raise TypeError("Expected a Contact object.")
        primary_data = contact.get_contact_formated()
        if primary_data is None:
            raise TypeError("Expected data in user")
        my_frame.insert(i, primary_data)
        i = i + 1


def delete_contact():
    global my_frame
    contact_data = my_frame.get()
    index = my_frame.curselection()
    my_frame.delete(index)
    user = get_user()
    user.delete_contact(contact_data)


def add_contact():
    global new_contact_screen
    new_contact_screen = customtkinter.CTkToplevel(birthday_screen)
    new_contact_screen.title("Add New Birthday")
    new_contact_screen.minsize(width=300, height=400)
    new_contact_screen.attributes('-topmost', True)

    global contact_entry_name
    global contact_entry_last_name
    global contact_entry_email
    global contact_entry_number
    global contact_entry_date

    contact_name = StringVar()
    contact_last_name = StringVar()
    contact_email = StringVar()
    contact_number = StringVar()
    contact_date = StringVar()

    customtkinter.CTkLabel(new_contact_screen, text="Enter new birthday data below").pack()
    customtkinter.CTkLabel(new_contact_screen, text="Name").pack()
    contact_entry_name = customtkinter.CTkEntry(new_contact_screen, textvariable=contact_name)
    contact_entry_name.pack()

    customtkinter.CTkLabel(new_contact_screen, text="Last Name").pack()
    contact_entry_last_name = customtkinter.CTkEntry(new_contact_screen, textvariable=contact_last_name)
    contact_entry_last_name.pack()

    customtkinter.CTkLabel(new_contact_screen, text="Email").pack()
    contact_entry_email = customtkinter.CTkEntry(new_contact_screen, textvariable=contact_email)
    contact_entry_email.pack()

    customtkinter.CTkLabel(new_contact_screen, text="number").pack()
    contact_entry_number = customtkinter.CTkEntry(new_contact_screen, textvariable=contact_number)
    contact_entry_number.pack()

    customtkinter.CTkLabel(new_contact_screen, text="Birthday date : yyyy-mm-dd").pack()
    contact_entry_date = customtkinter.CTkEntry(new_contact_screen, textvariable=contact_date)
    contact_entry_date.pack()

    customtkinter.CTkButton(new_contact_screen, text="Add user", width=10, height=1, command=submit_contact).pack()
    new_contact_screen.bind("<Return>", lambda event: submit_contact())
    global valid_label
    valid_label = customtkinter.CTkLabel(new_contact_screen, text="", text_color="red")
    valid_label.pack()


def submit_contact():
    name = contact_entry_name.get()
    last_name = contact_entry_last_name.get()
    email = contact_entry_email.get()
    number = contact_entry_number.get()
    date = contact_entry_date.get()
    valid_date = re.match(r"([0-9]{4}-[0-9]{2}-[0-9]{2})", date)
    if valid_date is None:
        valid_label.configure(text="Date must be in yyyy-mm-dd format", text_color="red")
    elif name == "":
        valid_label.configure(text="Name is required", text_color="red")
    else:
        string = date.split("-")
        year = int(string[0])
        month = int(string[1])
        day = int(string[2])
        date_formated = datetime.datetime(year, month, day)
        if date_formated <= datetime.datetime.now():
            global my_frame
            my_frame.pack_forget()
            user = get_user()
            user.add_contact(name, last_name, email, number, date)
            new_contact_screen.destroy()
            sync_contacts(user.get_contacts())
        else:
            valid_label.configure(text="Date must be in the past", text_color="red")


def register():
    global register_screen
    global register_button
    global username
    global username_entry
    global username_label
    global text_label  # Объявление переменной как глобальной

    register_screen = customtkinter.CTkToplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x200")
    register_screen.attributes('-topmost', True)

    global username
    global username_entry
    username = StringVar()

    text_label = customtkinter.CTkLabel(register_screen, text="Please enter details below",
                                        font=("calibri", 20, "bold"))
    customtkinter.CTkLabel(register_screen, text="").pack()
    text_label.pack()

    username_label = customtkinter.CTkLabel(register_screen, text="Enter username", font=("calibri", 20))
    username_label.pack()

    username_entry = customtkinter.CTkEntry(register_screen, textvariable=username, corner_radius=30)
    username_entry.pack()
    username_entry.bind("<Return>", lambda event: register_user())  # Привязка к клавише Enter
    customtkinter.CTkLabel(register_screen, text="").pack()

    register_button = customtkinter.CTkButton(register_screen, text="Register", width=100, height=35, corner_radius=30,
                                              command=register_user)
    register_button.pack()
    global info_label
    info_label = customtkinter.CTkLabel(register_screen, text="", font=("calibri", 11))
    info_label.pack()


def register_user():
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

    username_info = username.get().lower()
    username_entry.delete(0, END)
    if len(username_info) < 5:
        info_label.configure(text="Username must be 5 letters or longer", text_color="red")
    else:
        if check_exists(username_info):
            info_label.configure(text="Username already exists", text_color="red")
        else:
            dictionary = {"birthdays": []}
            json_object = json.dumps(dictionary)
            json_file_path = os.path.join(database_path, f"{username_info}.json")
            print(json_file_path)
            with open(json_file_path, "w") as outfile:
                outfile.write(json_object)
            info_label.configure(text="Registration Success", text_color="green", font=("calibri", 15))

            # Скрываем текст сверху, кнопку регистрации, поле ввода имени пользователя и надпись "Username"
            register_button.pack_forget()
            username_entry.pack_forget()
            username_label.pack_forget()
            text_label.pack_forget()

            # Создаем и отображаем кнопку "OK"
            ok_button = customtkinter.CTkButton(register_screen, text="OK", corner_radius=20,
                                                command=lambda: register_screen.destroy())
            ok_button.pack()

            # Привязка клавиши Enter к кнопке "OK"
            register_screen.bind("<Return>", lambda event: ok_button.invoke())


def login():
    global login_screen
    login_screen = customtkinter.CTkToplevel(main_screen)
    login_screen.title("Login")
    login_screen.minsize(width=300, height=200)
    login_screen.maxsize(width=300, height=200)
    login_screen.attributes('-topmost', True)

    customtkinter.CTkLabel(login_screen, text="Enter your username", font=("calibri", 20)).pack()
    customtkinter.CTkLabel(login_screen, text="").pack()

    global username_verify
    global username_login_entry
    username_verify = StringVar()

    customtkinter.CTkLabel(login_screen, text="Username", font=("calibri", 20)).pack()
    username_login_entry = customtkinter.CTkEntry(login_screen, textvariable=username_verify, corner_radius=30)
    username_login_entry.pack()
    username_login_entry.bind("<Return>", lambda event: login_user())  # Привязка к клавише Enter

    customtkinter.CTkLabel(login_screen, text="").pack()
    customtkinter.CTkButton(login_screen, text="Login", width=100, height=35, corner_radius=30,
                            command=login_user).pack()

    global login_label
    login_label = customtkinter.CTkLabel(login_screen, text="", font=("calibri", 11))
    login_label.pack()


def login_user():
    username_input = username_login_entry.get()
    username_input = username_input.lower()
    if not check_exists(username_input):
        login_label.configure(text="Username doesnt exists", text_color="red")
    else:
        global current_user
        login_screen.destroy()
        user = User(username_input)
        current_user = user
        birthday_app()


tray_icon.menu = (
    pystray.MenuItem("Open", restore_from_tray),
    pystray.MenuItem("Minimize", minimize_to_tray),
    pystray.MenuItem("Quit", close_application),
)

tray_icon_thread = threading.Thread(target=tray_icon.run)
tray_icon_thread.daemon = True
tray_icon_thread.start()

main_account_screen()

# pyinstaller --noconsole --add-data database:database app.py
