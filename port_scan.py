import tkinter as tk
import socket
from utils import *
from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


class PortScan:
   
    def __init__(self, text_window):
        self.open_ports = []
        self.closed_ports = []
        self.firewall_ports = []
        self.no_answer = []
        self.ip_address = ""
        self.text = text_window


    def port_scan(self, dest_port):
        src_port = random.randint(1025,65534)

        try:
            scan_params = IP(dst=self.ip_address)/TCP(sport=src_port, dport=dest_port, flags="S")

            scan_resp = sr1(scan_params, retry=1, timeout=1, verbose=0)

            if (str(type(scan_resp)) == "<class 'NoneType'>"):
                self.no_answer.append(dest_port)
                

            elif(scan_resp.haslayer(TCP)):

                if(scan_resp.getlayer(TCP).flags == 0x12):
                    self.open_ports.append(dest_port)
                    sr1(IP(dst=self.ip_address)/TCP(sport=src_port, dport=dest_port, flags="RA"), timeout=1, verbose=0)

                elif(scan_resp.getlayer(TCP).flags == 0x14):
                    self.closed_ports.append(dest_port)

            elif (scan_resp.haslayer(ICMP)):   

                if( int(scan_resp.getlayer(ICMP).type) == 3 and int(scan_resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
                    self.firewall_ports.append(dest_port)
 
        except Exception as error:
            print(str(dest_port) + " : " + str(error) )


    def host_ip(self, host_name):
        try:
            self.ip_address = socket.gethostbyname(host_name)

        except socket.gaierror as error:
            self.text.insert(tk.END, "Bad name error: \n" + str(error))
            
    def run(self, x, y, host_name, port_type, port2=0):

        self.text.delete("1.0", tk.END)

        self.no_answer = []
        self.open_ports = []
        self.closed_ports = []
        self.firewall_ports = []

        self.host_ip(host_name)

        if self.ip_address == "":
            self.text.insert(tk.END, "\nError reading the host name.")

        elif self.ip_address != None:
            if port_type == None:
                port_type = "common"

            if ((port_type == "common") or (port_type == "all")):
                ports = open_json(port_type)
            else:
                ports = create_ports_list(port_type, port2)

            if len(ports) != 0:
                
                threadpool(self.port_scan, ports.keys(), len(ports.keys()), x, y)

                self.open_ports.sort()
                self.closed_ports.sort()
                self.firewall_ports.sort()
                self.no_answer.sort()

                self.text.insert(tk.END, "Scanned IP: " + str(self.ip_address))  
                self.text.insert(tk.END, "\nReachable ports: " + str(len(self.open_ports) + len(self.closed_ports) + len(self.firewall_ports)) + " out of " + str(len(ports)) + " ports.")

                temp = port_service(self.open_ports)
                self.text.insert(tk.END, "\nOpen ports: ")

                if len(temp) > 0:
                    for item in temp:
                        self.text.insert(tk.END, "\n[" +str(item) + "] --> " + str(temp[item]))
                else:
                    self.text.insert(tk.END, "\n[]")


                self.text.insert(tk.END, "\nFirewall ports: \n" + str(self.firewall_ports))
                self.text.insert(tk.END, "\nClosed ports: \n" + str(self.closed_ports))
                self.text.insert(tk.END, "\nNo answer/filtered ports: \n" + str(self.no_answer))

            else:
                self.text.insert(tk.END, "Error reading the port(s). Try again.")

        else:
            self.text.insert(tk.END, "\nError reading the host name.")
