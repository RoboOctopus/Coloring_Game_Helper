import tkinter as tk
import ttkbootstrap as ttk
import time
import bot_v4
import os 
from tkinter import messagebox


set_res_x = 2560
set_res_y = 1440



dir_path = os.path.dirname(os.path.realpath(__file__))

resolution = []

def finished_time():
	messagebox.showerror('Finished', 'Here is some information')

     
def start():
    time.sleep(1)
    l = bot_v4.bot(dir_path,int(input_x.get()),int(input_y.get()))
    messagebox.showinfo('Finished', f'Time to complet: {l} s')

def close():
    (window.quit())


def set_x():
    #input_x.set('2160')
    output_xx = input_x.get()
    output_x.set(output_xx)
    print(output_xx)

def set_y():
    #input_y.set('1440')
    output_yy = input_y.get()
    output_y.set(output_yy)
    print(output_yy)


#window
window = ttk.Window(themename = 'darkly', position = (300,300))#, position = (4500,-500)
window.resizable(False,False)
window.title('Coloring Game helper')
window.geometry('300x210')
window.iconbitmap(f'{dir_path}/icon.ico')


#title
title_lable = ttk.Label(master = window, text = 'Resolution:', font = 'Calibri 14')
title_lable.pack()

input_x = tk.StringVar()
input_y = tk.StringVar()

# widgets 
res_set = ttk.Frame(master= window, padding= 12)

res_x = ttk.Frame(master= res_set)
res_y = ttk.Frame(master= res_set)

entry_x = ttk.Entry(master = res_x, textvariable = input_x, width= 6)
entry_x.pack()
set_button = ttk.Button(master = res_x, text = 'enter', command = set_x)
set_button.pack()
res_x.pack(side= 'left')

entry_y = ttk.Entry(master = res_y, textvariable = input_y, width= 6)
entry_y.pack()
button = ttk.Button(master = res_y, text = 'enter', command = set_y)

res_y.pack()
res_set.pack()
button.pack()


output_x = tk.StringVar()
output_y = tk.StringVar()

input_x.set(set_res_x)
input_y.set(set_res_y)

output_x.set('height')
output_y.set('width')


display = ttk.Frame(master= window)

output_label_x = ttk.Label(master = display,   text = 'output_label_x',   font = 'Calibri 16',   textvariable = output_x)
output_label_x.pack(side= 'left')
ex  = ttk.Label(master = display,   text = 'x',   font = 'Calibri 16')
ex.pack(side= 'left')
output_label_y = ttk.Label(master = display,   text = 'output_label_y',   font = 'Calibri 16',   textvariable = output_y)
output_label_y.pack(side= 'left')




display.pack()


#start and close button
button_start = ttk.Button(master = window, text = 'Start',command = start, width= 8)
button_close = ttk.Button(master = window, text = 'Close', command = close, width= 8)
button_start.pack(side= 'left', padx= 53)
button_close.pack(side = 'left', padx=0)


# run 
window.mainloop()