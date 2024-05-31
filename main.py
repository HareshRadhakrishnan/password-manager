from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [  random.choice(letters) for _ in range(nr_letters) ]
    password_symblos =[random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_numbers + password_symblos + password_letters
    random.shuffle(password_list)

    password = "".join(password_list)
    txt_psk.insert(0,password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def Save():
    Site = txt_site.get()
    email =txt_mail.get()
    password = txt_psk.get()
    data_values={
         Site : {
            "email":email,
            "password":password
        }
    }
    if len(txt_psk.get())==0 or len(txt_site.get())==0:
        print(len(txt_psk.get()))
        messagebox.showinfo(title="Oops",message="Don't Leave the Fields empty ")
        return
    is_ok = messagebox.askokcancel(title=txt_site.get(),message=f"These are the details:\nEmail:{txt_mail.get()}\nPassword:{txt_psk.get()}\n Is it ok to save?")
    if is_ok:
        try:
            with open("logs.json", "r") as file:
                data=json.load(file)
                data.update(data_values)
        except FileNotFoundError:
            with open("logs.json","w") as file:
                data = data_values
                json.dump(data,file,indent=4)
        finally:
            with open("logs.json","w") as file:
                json.dump(data,file,indent=4)
        txt_psk.delete(0, END)
        txt_site.delete(0, END)
# ---------------------------- Search Password ------------------------------- #
def find_psk():
    try:
        with open("logs.json" ,"r") as file:
            data = json.load(file)[txt_site.get()]
    except KeyError:
        messagebox.showinfo(title=txt_site.get(), message=f"You Have not saved the credentials of{txt_site.get()}")
    except FileNotFoundError:
        messagebox.showinfo(title=txt_site.get(), message=f"No Information Found")
    else:
        mail = data["email"]
        psk = data["password"]
        messagebox.showinfo(title=txt_site.get(), message=f"These are the details:\nEmail:{mail}\nPassword:{psk}")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)
canvas = Canvas(height=200,width=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0,column=1)

lbl_site =Label(text="Website:")
lbl_site.grid(row=1, column=0)
lbl_mail =Label(text="Email/Username:")
lbl_mail.grid(row=2, column=0)
lbl_psk =Label(text="Password:")
lbl_psk.grid(row=3, column=0)

txt_site = Entry(width=35)
txt_site.grid(row=1,column=1)
txt_mail = Entry(width=70)
txt_mail.grid(row=2,column=1,columnspan=4)
txt_mail.insert(0,"haresh2569@gmail.com")
txt_psk = Entry(width=35)
txt_psk.grid(row=3,column=1)

btn_generate = Button(text="Generate Password", command=pass_gen,width=35)
btn_generate.grid(row=3,column=2)
btn_add = Button(text="Add",width=70,command=Save)
btn_add.grid(row=4,column=1,columnspan=2)
btn_search = Button(text="Search",width=30,command=find_psk)
btn_search .grid(row=1,column=2)

window.mainloop()