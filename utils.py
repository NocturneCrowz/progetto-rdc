import tkinter as tk
from tkinter import ttk
from multiprocessing.pool import ThreadPool
from multiprocessing import freeze_support
import os
import json

def open_json(value):

    if value == "common":
        path = "./common_ports.json"

        with open(path) as file:
            ports_info = json.load(file)
    
        ports = {int(k): v for (k, v) in ports_info.items()}

    elif value == "all":
        ports = {}
        for i in range (1, 65535):
            ports[i] = None

    return ports

def create_ports_list(port1, port2):

    ports = {}

    if type(port1) == list:
 
        for port in port1:
            ports[port] = None

    elif (port2 != 0) and (port2 > port1):
        
        for i in range (port1, port2+1):
            ports[i] = None

    elif (port1 == port2) or (port1 != 0 and port2 == 0):
        
        ports[port1] = None

    else:
        
        print("Problem reading the ports")
        pass

    return ports


def port_service(list):
    services = open_json("common")
    ret_list = {}

    for list_item in list:
        if list_item in services.keys():
            ret_list[list_item] = services[list_item]
        else:
            ret_list[list_item] = "unknown"

    return ret_list

        


def threadpool(function, iterable, iterable_length, x, y):
    workers = os.cpu_count()

    popup = tk.Toplevel()
    tk.Label(popup, text="Scanning ports").grid(row=0,column=0)
    
    popup.wm_overrideredirect(True)
    progress = 0
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100, length=300)
    progress_bar.grid(row=1, column=0)
    popup.pack_slaves()
    popup.geometry("%+d%+d" % (x + 300, y + 200))
    progress_step = float(100.0/iterable_length)


    print("Running with " + str(workers) + " workers.")

    with ThreadPool(workers) as pool:

        try:

            for loop_index, _ in enumerate(pool.imap(function, iterable)):
                             
                freeze_support()
                popup.update() 
                progress += progress_step
                progress_var.set(progress)
                tk.Label(popup, text=("%.1f" % (loop_index / iterable_length * 100.0) + "%" )).grid(row=3, column=0)
                
        except Exception as e:
            print(e)

        popup.destroy()
