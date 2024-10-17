from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    password_entry.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_list = [choice(letters) for i in range(randint(8, 10))]
    password_list += [choice(symbols) for j in range(randint(2, 4))]
    password_list += [choice(numbers) for k in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get().title()
    email = email_entry.get() 
    password = password_entry.get()
    
    new_data = {
        website : {
            "Email" : email,
            "Password" : password,
        }
    }
    
    if len(website) == 0 or len(password) == 0 :
        return messagebox.showinfo(title= "Oops", message= "Please don't leave any fields empty!")

    is_ok = messagebox.askokcancel(title= website, message= f"These are the details entered: \nEmail: {email}"
                                   f"\nPaswword: {password} \nIs it ok to save? ")

    if is_ok:
        try:
            with open ("data.json", mode= "r") as file :
                data = json.load(file) 
                data.update(new_data)
        except FileNotFoundError :
            with open ("data.json", mode= "w") as file :
                json.dump(new_data, file, indent= 4)  
        else: 
            with open ("data.json", mode= "w") as file :
                json.dump(data, file, indent= 4)  
        finally :  
            website_entry.delete(0,END)
            password_entry.delete(0,END)  
            
# ---------------------------- SEARCH FUNCTIONALITY ------------------------------- #           

def find_password():  
    try:
        website = website_entry.get().title()
        with open ("data.json") as data_file :
            data = json.load(data_file)           
    except FileNotFoundError :
        return messagebox.showinfo(title= "Error", message= "No data file found.") 
    else:
        if website in data :
            website_info = data[website]
            email = website_info["Email"]
            password = website_info["Password"]
            return messagebox.showinfo(title= f"{website}", message= f"Email: {email} \nPassword: {password}")
        else : 
            return messagebox.showinfo(title= "Oops", message= f"No details for {website} exists.")
        
                
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady= 50)

canvas = Canvas(width= 200, height= 200 )
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100, image = logo)
canvas.grid(row=0, column= 1)

# Website widgets
website_label = Label(text= "Website:")
website_label.grid(row=1, column= 0)

website_entry = Entry(width=34)
website_entry.focus()
website_entry.grid(row=1, column=1)

# email widgets
email_label = Label(text= "Email/Username:")
email_label.grid(row=2, column= 0)

email_entry = Entry(width=52)
email_entry.insert(0,"user@gmail.com")
email_entry.grid(row=2, column=1, columnspan= 2)

#password widgets
password_label = Label(text= "Password:")
password_label.grid(row=3, column= 0)

password_entry = Entry(width=34)
password_entry.grid(row=3, column=1)

password_button = Button(text="Generate Password", command= password_generator)
password_button.grid(row= 3, column=2)

#search button
search_button = Button(text="Search",width= 14, command= find_password)
search_button.grid(row= 1, column=2 )

add_button = Button(text="Add", width=44, command= save)
add_button.grid(row= 4, column=1, columnspan= 2)


window.mainloop()
