#requires python 3.8+ may work on 3.6, 3.7 definitely broken on <= 3.5 due to subprocess args (text=True)
from tkinter import *
from tkinter.ttk import *
import subprocess
import sys
import re

DEVICE_COLUMNS = ["bus_id", "manufacturer", "description"]
USBIPD_PORT = 3240

def init_kernel_modules():
	subprocess.run(["sudo", "modprobe", "usbip_host"])
	subprocess.run(["sudo", "modprobe", "usbip_core"])
	subprocess.run(["sudo", "modprobe", "vhci_hcd"])

def scan():
	#TODO
	return 0

def refresh_local():
	local_devices = list_local_usb()
	local_listbox.delete(*local_listbox.get_children())
	for device in local_devices:
		local_listbox.insert('', "end", values=device)

def refresh_remote():
	server_ip = remote_ip_input.get()
	remote_devices = list_remote_usb(server_ip)
	remote_listbox.delete(*remote_listbox.get_children())
	for device in remote_devices:
		remote_listbox.insert('', "end", values=device)

def bind_local():
	selection = local_listbox.selection()
	result = bind_local_usb(selection[0])

def unbind_local():
	selection = local_listbox.selection()
	result = unbind_local_usb(selection[0])

def attach_remote():
	server_ip = remote_ip_input.get()
	selection = remote_listbox.selection()
	print(server_ip)
	print(selection[0])
	print(selection)
	print(remote_listbox.item(selection[0]))
	bus_id = remote_listbox.item(selection[0])['values'][0]
	print(bus_id)
	result = attach_remote_usb(server_ip, bus_id)
	refresh_remote()
	refresh_local()

def detach_remote():
	detach_remote_usb()
	refresh_remote()
	refresh_local()


#def start_usbipd():
#gksudo
#	subprocess.run("sudo usbipd")

def parse_local_list(text):
	rows = []
	devices = text.strip().split("\n\n")
	for device in devices:
		#print(device)
		lines = device.strip().split("\n")
		#print(lines)
		bus_info = lines[0].split(" ")
		man_info = lines[1].split(":")
		'''rows.append({
			'bus_id': bus_info[2],
			'addr': bus_info[3],
			'manufacturer': man_info[0],
			'description': man_info[1]
		})'''
		rows.append((
			bus_info[2],
			#bus_info[3],
			man_info[0],
			man_info[1]
		))
	#print(rows)
	return rows

def parse_remote_list(text):
	if text.__contains__("no exportable devices found on") == True:
		return []

	rows = []

	busid_regex = re.compile("^\d+-\d+$|^\d+-\d+\.\d+$")
	lines = text.strip().split("\n")
	for line in lines:
		vals = line.strip().split(":")
		print(vals)
		m = busid_regex.match(vals[0])
		if m: #the first value is a bus_id, grab the info
			rows.append((
				vals[0],
				vals[1],
				vals[2]
			))
	return rows

def list_local_usb():
	result = subprocess.run(["usbip", "list", "--local"], capture_output=True, text=True)
	return parse_local_list(result.stdout)


def list_remote_usb(server_ip):
	result = subprocess.run(["usbip", "list", "--remote="+server_ip], capture_output=True, text=True)
	return parse_remote_list(result.stdout)

def bind_local_usb(bus_id):
	result = subprocess.run(["usbip", "bind", "--busid="+bus_id], capture_output=True, text=True)
	print(result.stdout)

def unbind_local_usb(bus_id):
	result = subprocess.run(["usbip", "unbind", "--busid="+bus_id], capture_output=True, text=True)
	print(result.stdout)

def attach_remote_usb(server_ip, bus_id):
	result = subprocess.run(["usbip", "attach", "--remote="+server_ip, "--busid="+bus_id], capture_output=True, text=True)
	print(result.stdout)
	print(result.stderr)
	return result

def detach_remote_usb(port=USBIPD_PORT):
	result = subprocess.run(["usbip", "detach", "--port="+str(port)], capture_output=True, text=True)
	print(result.stdout)
	print(result.stderr)

#def update_list(list, values):


#class UsbIpGui():

#	def __init__(self):
root = Tk()
root.wm_title("USB/IP Peer")
root.geometry("1040x480")

#TODO listbox for remote (from entered IP) usb items
remote_control_frame = Frame(root)
remote_list_label = Label(remote_control_frame, text="Remote USB Devices for ")
remote_ip_input = Entry(remote_control_frame)
remote_list_refresh_button = Button(remote_control_frame, text="Refresh", command=refresh_remote)
remote_list_attach_button = Button(remote_control_frame, text="Attach Device", command=attach_remote)
remote_list_detach_button = Button(remote_control_frame, text="Detach All Devices", command=detach_remote)

remote_listbox = Treeview(columns=DEVICE_COLUMNS, show="headings")#Listbox(root)
#remote_listbox.pack(side="left")

for col in DEVICE_COLUMNS:
	remote_listbox.heading(col, text=col.title())

remote_devices = list_remote_usb('127.0.0.1')#'192.168.1.103')
for device in remote_devices:
	remote_listbox.insert("", "end", values=device)

remote_list_label.grid(column=0, row=0)
remote_ip_input.grid(column=1, row=0)
remote_list_refresh_button.grid(column=2, row=0)
remote_list_attach_button.grid(column=3, row=0)
remote_list_detach_button.grid(column=4, row=0)

remote_control_frame.grid(column=0, row=0)
remote_listbox.grid(column=0, row=1)

#TODO listbox for local items

local_control_frame = Frame(root)
local_list_label = Label(local_control_frame, text="Local USB Devices")
local_list_refresh_button = Button(local_control_frame, text="Refresh", command=refresh_local)
local_list_bind_button = Button(local_control_frame, text="Bind Device", command=bind_local)
local_list_unbind_button = Button(local_control_frame, text="Unbind Device", command=unbind_local)
local_listbox = Treeview(columns=DEVICE_COLUMNS, show="headings")#Listbox(root)


#local_listbox.pack(side="right")

#setup column names
for col in DEVICE_COLUMNS:
	local_listbox.heading(col, text=col.title())
	#local_listbox.column(col, width=tkFont)

local_devices = list_local_usb()
for device in local_devices:
	local_listbox.insert('', "end", values=device)


local_list_label.grid(column=0, row=0)
local_list_refresh_button.grid(column=1, row=0)
local_list_bind_button.grid(column=3, row=0)
local_list_unbind_button.grid(column=4, row=0)

local_control_frame.grid(column=0, row=2)
local_listbox.grid(column=0, row=3)

'''
#TODO listbox for attached items and their respective servers
attached_list_label = Label(root, text="Attached USB Devices")
attached_listbox = Listbox(root)
#attached_listbox.pack(side="right")

attached_list_label.grid(column=2, row=0)
attached_listbox.grid(column=2, row=1)
'''
#TODO scan button
'''scan_button = Button(root, text="Scan", command=scan)
scan_button.pack(side="bottom")

#TODO refresh button 
refresh_button = Button(root, text="Refresh", command=refresh)
refresh_button.pack(side="bottom")
'''

		

list_local_usb()

root.mainloop()


