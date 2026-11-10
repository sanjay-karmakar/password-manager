from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    list_of_letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ];
    list_of_symbols = ["!", "@", "#", "$", "%", "^", "&", "*"];
    list_of_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"];

    password_letters = [random.choice(list_of_letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(list_of_symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(list_of_numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)
    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_dict = {
        website: {
            "email": email,
            "password": password
        }
    }

    # FIXED: Added length check for email just in case
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                # 1. Try to open and read existing file data --> json.load()
                with open("data.json", "r") as data_file:
                    data = json.load(data_file);

            except FileNotFoundError:
                # 2. If FILE NOT FOUND, create it and write the data for the first time
                with open("data.json", "w") as data_file:
                    json.dump(new_dict, data_file, indent=4)

            else:
                # 3. If FILE FOUND, update data with old data
                data.update(new_dict)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- Find Password ------------------------------- #
def find_password():
    website = website_entry.get()

    with open("data.json") as data_file:
        data = json.load(data_file)
        
        if website in data:
            print(data)
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"{email}\n{password}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Website Label and Entry
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry(width=43)
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.focus()

# Search button
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")

# Email/Username Label and Entry
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_entry = Entry(width=35)
email_entry.insert(0, "your_email@example.com")
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

# Password Label and Entry
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=25)
password_entry.grid(column=1, row=3, sticky="EW")

gen_password_button = Button(text="Generate Password", width=14, command=generate_password)
gen_password_button.grid(column=2, row=3, sticky="EW")


# Add Button
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")





window.mainloop()