import subprocess
import random

try:
	# noinspection PyUnresolvedReferences
	import win10toast
except ImportError:
	pass

# <editor-fold desc="Initializers">
try:
	tst = win10toast.ToastNotifier()
except:
	pass

def toast(notification, title="ADB Tools", icon_path = None, duration=3):
	try:
		tst.show_toast(title, notification, icon_path, duration)
	except:
		pass
	
	#TODO: Most of the functions need to ignore TCP devices
	
def _command_connect_helper(device):
	c.ip_addr(device, ip=_command_local_ip_helper(device))
	cmd.tcp_ip.call(device=device)
	return c.ip_addr(device) + ":" + c.get_tcp_port(device)

def _command_disconnect_helper(device):
	return c.ip_addr(device) + ":" + c.get_tcp_port(device)

def _command_usb_helper(device):
	return c.ip_addr(device) + ":" + c.get_tcp_port(device)

def _command_local_ip_helper(device):
	if device in c.connected_ip_addr.keys():
		return c.ip_addr(device)
	else:
		result = cmd.local_ip.call(device=device)
		result = result.strip()
		for line in result.split("\n"):
			line = line.strip()
			if line.startswith("inet "):
				l = line.split(" ")
				return (l[1]).split("/")[0]
	
# </editor-fold>

class config:
	sleep = 1
	tcp_port = "50155"
	tcp_port_range=(50001,63000)
	random_port = False
	
	connected_ip_addr = {}
	used_tcp_ports = {}
	
	def get_tcp_port(self, device):
		if device in self.used_tcp_ports.keys():
			return self.used_tcp_ports[device]
		if not self.random_port:
			while self.tcp_port in self.used_tcp_ports:
				self.tcp_port = str(int(self.tcp_port) + 2)
			self.used_tcp_ports[device] = self.tcp_port
			return self.tcp_port
		else:
			while self.tcp_port in self.used_tcp_ports:
				self.tcp_port = str(random.randint(*self.tcp_port_range, 2))
			self.used_tcp_ports[device] = self.tcp_port
			return self.tcp_port
		
	def ip_addr(self, device, ip=None):
		if device in self.connected_ip_addr.keys():
			return self.connected_ip_addr[device]
		else:
			self.connected_ip_addr[device] = str(ip)
			
	def get_device_count(self, devices):
		count = 0
		for device in devices:
			if ":" not in device:
				if not self.is_duplicate_device(device):
					count += 1
		return count
	
	def is_duplicate_device(self, device):
		if device in self.connected_ip_addr.keys() and device in self.used_tcp_ports.keys():
			return True
		else:
			return False
	
	@staticmethod
	def join(*args):
		return " ".join([*args])

def shell(_cmd, stdout=True):
	pipe = subprocess.check_output(_cmd, shell = True)
	if stdout:
		print(pipe.decode())
	return pipe

class command:
	def __init__(self, value):
		self.value = "adb " + value
		self.pipe = None
		self.output = None
	
	def __repr__(self):
		return self.output
	
	def call(self, *, stdout = True):
		if self.pipe is None:
			self.pipe = shell(self.value, stdout)
		self.output = self.pipe.decode()
		return self.output

class device_command:
	def __init__(self, value, function=None):
		self.value = value
		self.pipe = None
		self.output = None
		self.func = function
	
	def __repr__(self):
		return self.output
	
	def call(self, *, device=None, stdout=True):
		if self.func is None:
			value = "adb -s " + device.strip() + " " + self.value
		else:
			value = "adb -s " + device.strip() + " " + self.value + " " + self.func(device.strip())
		if self.pipe is None:
			self.pipe = shell(value, stdout)
		self.output = self.pipe.decode()
		return self.output

class commands:
	def __init__(self):
		#Local Commands
		self.start_server = command("start-server")
		self.kill_server = command("kill-server")
		self.devices = command("devices")
		
		#Device Commands
		self.mtp = device_command("shell svc usb setFunctions mtp true")
		self.usb = device_command("usb", _command_usb_helper) #Disables the remote TCP/IP port
		self.disconnect = device_command("disconnect", _command_disconnect_helper) #Disconnects from device locally
		self.tcp_ip = device_command("tcpip", c.get_tcp_port)
		self.connect = device_command("connect", _command_connect_helper)
		self.local_ip = device_command("shell ip addr show wlan0")
	
	def get_devices(self, ignore_emulators=True):
		def get_device(string):
			device_id = string.split("\t")[0]
			if len(device_id) > 0:
				return device_id
			
		device_list = []
		
		out = self.devices.call()
		for line in out.split("\n"):
			line=line.rstrip()
			if line == "" or len(line)<1:
				continue
			if "List of devices attached" not in line:
				if not ignore_emulators and line.startswith("emulator"): #Emulator inclusive
					device_list.append(get_device(line))
				else: #Emulators are ignored
					device_list.append(get_device(line))
		return device_list
		
# <editor-fold desc="Post-Initializers">
c = config()
cmd = commands()
# </editor-fold>

d = cmd.get_devices()
for i in d:
	if ":" not in i:
		cmd.connect.call(device = i)

"""q = 0
while q < 2:
	cmd.devices.call()
	d = cmd.get_devices()
	for i in d:
		if not c.is_duplicate_device(i):
			print("a      a")
			cmd.connect.call(device=i)
		else:
			print("b     b")
			if ":" in i:
				print(i)
				cmd.usb.call(device=i)
				cmd.devices.call()
	dvc = c.get_device_count(d)
	if dvc > 0:
		if dvc == 1:
			toast("1 device found")
		else:
			toast(str(dvc) + " devices found")
	
	q += 1
"""