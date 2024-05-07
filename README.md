# **Introduction**


The program is a simple GUI application that assists in tracking your friends and siblings birthdays. In the program, you can create multiple accounts to create a separation between birthdays if several people use the same program at once.

It is written in Python and uses the `tkinter` and its extensions `customtkinter` libraries to create the GUI.

To run the program, you need Python 3.11 or later. You can open the program by using either `Visual Studio Code` or `PyCharm`, by using their inbuilt run operations. Alternatively, you have the option to download the compiled program from `Tags - 1.0`.

## Program Functionality


The program allows users to:

- **Create Accounts**: Each user can create a personal account to manage their own set of birthdays.
- **Save Birthdays**: Once logged in, users can add and save birthdays to their account.
- **View Birthdays**: Users can view all saved birthdays in a list within the main window.
- **Edit Birthdays**: Users have the option to edit or delete any saved birthday information.
- **Search Functionality**: There is a search bar to quickly find a specific birthday by name.
- **Notifications**: The program can be set to give notifications as reminders for upcoming birthdays.
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
