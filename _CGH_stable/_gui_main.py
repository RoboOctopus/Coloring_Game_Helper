import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk
import keyboard as kb
import bot_v4
import os 
from tkinter import messagebox
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

resolution = []

def finished_time():
	messagebox.showerror('Finished', 'Here is some information')

def set_res_720p():   
    config_file = open(f'{dir_path}\config.json', "w")

    json.dump(720,config_file, indent = 6)
    config_file.close()
    output_string.set(f'{json_in()}p')

def set_res_1080p():   
    config_file = open(f'{dir_path}\config.json', "w")
    json.dump(1080, config_file, indent = 6)
    config_file.close()
    output_string.set(f'{json_in()}p')

def set_res_1440p():   
    config_file = open(f'{dir_path}\config.json', "w")
    json.dump(1440, config_file, indent = 6)
    config_file.close()
    output_string.set(f'{json_in()}p')

def set_res_2160p():   
    config_file = open(f'{dir_path}\config.json', "w")
    json.dump(2160, config_file, indent = 6)
    config_file.close()
    output_string.set(f'{json_in()}p')

def json_in():
    config_file = open(f'{dir_path}\config.json', "r")
    list = json.load(config_file)
    config_file.close()
    return list
     
def start():
    print()
    l = bot_v4.bot(dir_path)
    messagebox.showinfo('Finished', f'Time to complet: {l} s')

def close():
    (window.quit())


# window
window = ttk.Window(themename = 'darkly', position = (500,500))
window.resizable(False,False)
window.title('Coloring Game helper')
window.geometry('300x210')
window.iconbitmap(f'{dir_path}/icon.ico')


# title
title_lable = ttk.Label(master = window, text = 'Game resolution:', font = 'Calibri 14')
title_lable.pack()


# input field
input_frame = ttk.Frame(master = window)

button_720p = ttk.Button(master = input_frame, text = '720p', command = set_res_720p)
button_1080p = ttk.Button(master = input_frame, text = '1080p', command = set_res_1080p)
button_1440p = ttk.Button(master = input_frame, text = '1440p', command = set_res_1440p)
button_2160p = ttk.Button(master = input_frame, text = '2160p', command = set_res_2160p)
button_720p.pack(side = 'left')
button_1080p.pack(side = 'left')
button_1440p.pack(side = 'left')
button_2160p.pack(side = 'left')
input_frame.pack()


# output
output_string = tk.StringVar(value = f'{json_in()}p')
output_label = ttk.Label(
    master = window,
    text = 'Output',
    font = 'Calibri 16',
    textvariable = output_string)
output_label.pack(pady = 15)


# start and close button
button_start = ttk.Button(master = window, text = 'Start',command = start, width= 8)
button_close = ttk.Button(master = window, text = 'Close', command = close, width= 8)
button_start.pack(side= 'left', padx= 53)
button_close.pack(side = 'left', padx=0)


# run 
window.mainloop()
    
