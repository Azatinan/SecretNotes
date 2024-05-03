import tkinter
from tkinter import END
from tkinter import messagebox
import base64

from PIL import ImageTk, Image

window = tkinter.Tk()
window.title("Secret Notes")
window.minsize(width=300, height=520)


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def save_and_encrypt_notes():
    title = my_entry_1.get()
    message = my_text.get("1.0", END)
    master_key = my_entry_2.get()

    if len(title) == 0 or len(message) == 0 or len(master_key) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all info.")
    else:
        message_encrypted = encode(master_key, message)
        try:
            with open("mysecret.txt", "a") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}")
        except FileNotFoundError:
            with open("mysecret.txt", "w") as data_file:
                data_file.write(f"\n{title}\n{message_encrypted}")
        finally:
            my_entry_1.delete(0, END)
            my_text.delete("1.0", END)
            my_entry_2.delete(0, END)


def decrypt_notes():
    message_encrypted = my_text.get("1.0", END)
    master_key = my_entry_2.get()

    if len(message_encrypted) == 0 or len(master_key) == 0:
        messagebox.showinfo(title="Error!", message="Please enter all information.")
    else:
        try:
            decrypted_message = decode(master_key, message_encrypted)
            my_text.delete("1.0", END)
            my_text.insert("1.0", decrypted_message)
        except:
            messagebox.showinfo(title="Error!", message="Please make sure of encrypted info.")


def resize_image(image_path, width, height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)


image = resize_image("Unknown.png", 100, 90)

# label
image_label = tkinter.Label(window, image=image)
image_label.pack()

my_label_1 = tkinter.Label(text="Enter your title")
my_label_1.place(x=100, y=100)

my_label_2 = tkinter.Label(text="Enter your secret")
my_label_2.place(x=90, y=160)

my_label_3 = tkinter.Label(text="Enter master key")
my_label_3.place(x=90, y=385)

# entry
my_entry_1 = tkinter.Entry(width=20)
my_entry_1.place(x=60, y=125)

my_entry_2 = tkinter.Entry(width=20)
my_entry_2.place(x=50, y=410)

# text
my_text = tkinter.Text(width=35, height=15)
my_text.place(x=20, y=180)

# button
my_button_1 = tkinter.Button(text="Save & Encrypt", width=8, command=save_and_encrypt_notes)
my_button_1.place(x=100, y=440)

my_button_2 = tkinter.Button(text="Decrypt", width=5, command=decrypt_notes)
my_button_2.place(x=110, y=470)

window.mainloop()
