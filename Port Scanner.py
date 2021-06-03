import tkinter as tk
from port_scan import PortScan
from multiprocessing import freeze_support

def clear():
    textwidget.delete("1.0", tk.END)

def start():
    port_scan.run(window.winfo_x(), window.winfo_y(), host_name.get(), "common")

def all():
    port_scan.run(window.winfo_x(), window.winfo_y(), host_name.get(), "all")

def single():
    port_scan.run(window.winfo_x(), window.winfo_y(), host_name.get(), int(single_entry.get()))

def range():
    port_scan.run(window.winfo_x(), window.winfo_y(), host_name.get(), int(range_entry1.get()), int(range_entry2.get()))

def retry():
    port_scan.run(window.winfo_x(), window.winfo_y(), host_name.get(), list(port_scan.no_answer))


if __name__ == '__main__': 
    freeze_support()
    window = tk.Tk()
    window.geometry("900x650")
    window.title("Port Scanner")
    window.grid_columnconfigure(0, weight=1)
    window.resizable(True, True)


    title = tk.Label(font = "Helvetica 16 bold", text="Port Scanner Multithread")
    title.grid(row=0,column=0)

    credits = tk.Label(window, text="Made by Cristian Barzotti")
    credits.place(relx=0.5, rely=0.95, anchor="center")

    host_name = tk.Entry()
    host_name.insert(tk.END, "scanme.nmap.org")
    host_name.grid(row=1, column=0, sticky="WE", padx=10)

    textwidget = tk.Text()
    textwidget.insert(tk.END, "For educational purpose only. \nScanning ports could be seen as \"inappropriate\", make sure you have the authorizations from the host.\n\nInsert the preferred host name, or click \"Run\" to use scanme.nmap.org.")
    textwidget.grid(row=5,  column=0, sticky="WE", padx=10, pady=10)

    tcp_button = tk.Button(text="Common Ports", command=start, width=30)
    tcp_button.grid(row=2, column=0, sticky="W", pady=10, padx=10)

    single_button = tk.Button(text="Single Port", command=single, width=30)
    single_button.grid(row=3, column=0, sticky="W", pady=10, padx=10)

    single_entry = tk.Entry(width=5)
    single_entry.grid(row=3, column=0, sticky="W", pady=10, padx=250)    
        
    range_button = tk.Button(text="Ports Range", command=range, width=30)
    range_button.grid(row=4, column=0, sticky="W", pady=10, padx=10)

    range_entry1 = tk.Entry(width=5)
    range_entry1.grid(row=4, column=0, sticky="W", pady=10, padx=250)

    range_label = tk.Label(text="to")  
    range_label.grid(row=4, column=0, sticky="W", pady=10, padx=290)

    range_entry2 = tk.Entry(width=5)
    range_entry2.grid(row=4, column=0, sticky="W", pady=10, padx=310)
    
    all_button = tk.Button(text="All", command=all, width=30)
    all_button.grid(row=2, column=0, sticky="E", pady=10, padx=10)

    retry_button = tk.Button(text="Retry", command=retry, width=30)
    retry_button.grid(row=3, column=0, sticky="E", pady=10, padx=10)

    clear_button = tk.Button(text="Clear", command=clear, width=30)
    clear_button.grid(row=4, column=0, sticky="E", pady=10, padx=10)


    port_scan = PortScan(textwidget)
    window.mainloop()

