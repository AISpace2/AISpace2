from ._version import version_info, __version__, update_notification, get_web_version
from tkinter import *

#create pop-up window reminding of newer version of AISpace2.
web_version = get_web_version()
if update_notification and __version__ != web_version:
    txt = ("Your current version is " + __version__ +
     " and the latest version is " + web_version  + 
     ". We recommend updating your AISpace2.")
    
    #create Tk pop-up window with the described formating.
    master = Tk() 
    Label(master, text=txt).grid(row=0, sticky=W)
    var1 = IntVar()
    Checkbutton(master, text="Check box if you wish not to be notified in the future.", variable=var1).grid(row=1, sticky=W)
    Button(master, text='Close', command=master.quit).grid(row=3, sticky=W, pady=4)
    mainloop()
    master.destroy()

    #update update_notification depending on wheather check button is checked.
    if var1 == 1:
        update_notification = False
    else:
        update_notification = True
    

"""
def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'aispace2',
        'require': 'aispace2/extension'
    }]
"""
