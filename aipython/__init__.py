from aispace2._version import __version__, need_update, toggle_update, get_web_version
from tkinter import *
import os

#create pop-up window reminding of newer version of AISpace2.
if need_update():
    web_version = get_web_version()
    txt = ("Your current version is " + __version__ +
     " and the latest version is " + web_version  + 
     ". We recommend updating your AISpace2.")
    
    #find path to application icon (.ico)
    root_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(root_path, '..\\misc\\AISpace2_Logo.ico')

    #create Tk pop-up window with the described formating.
    master = Tk() 
    master.title("AISpace2")
    master.iconbitmap(icon_path)
    Label(master, text=txt).grid(row=0, sticky=W)
    var = BooleanVar()
    cb = Checkbutton(master, text="Don't show this again.", variable=var, offvalue = False, onvalue = True)
    cb.grid(row=1, sticky=W)
    Button(master, text='Close', command=master.quit).grid(row=3, sticky=W, pady=4)
    mainloop()
    master.destroy()

    #update update_notification depending on wheather check button is checked.
    if var.get():
        toggle_update()