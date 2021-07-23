import os
import sys

class Utilities:
	@staticmethod
	def _unify(string):
		string = string.replace("\n", "")
		if string.startswith("#"):
			return "#" + string.lstrip("#").lstrip().rstrip()
		elif "=" in string:
			return "=".join([a.lstrip().rstrip() for a in string.split("=")])
		else:
			return string
	
	@staticmethod
	def _resolve(_path):
		if sys.platform == "win32":
			if len(_path) > 255:
				if not _path.startswith("\\\\?\\"):
					_path = "\\\\?\\" + _path
			return _path
		else:
			return _path
		
	def _check_file(self, _path):
		_path = self._resolve(_path)
		return os.path.exists(_path) and os.path.isfile(_path)
	
	def _ensure_file(self, _path):
		if not self._check_file(_path):
			open(_path, "w+").close()
		return _path
	
	def _clear_file(self, _path):
		if self._check_file(_path):
			with open(_path, "r+") as f:
				f.truncate(0)
	
	def _check_dir(self, _path):
		_path = self._resolve(_path)
		return os.path.exists(_path) and os.path.isdir(_path)
	
	def _ensure_dir(self, _path):
		_path = self._resolve(_path)
		if not self._check_dir(_path):
			os.mkdir(_path)
		return _path

class ShadowFile(Utilities):
	_string_data = ""
	_data = {}
	_own_path = ""
	
	def __init__(self, own_path, data=None):
		super().__init__()
		self._own_path = own_path
		
		#Ensure that data is read from the file if not provided
		if data is None:
			with open(super()._ensure_file(own_path), "r+") as f:
				self._string_data = f.read()
		else:
			if isinstance(data, list): #Ensure that data is actually a string
				assert isinstance(data, list)
				for n in range(len(data)):
					data[n] = str(data[n]).rstrip("\n").rstrip("\n")
				data = "\n".join(data)
			self._string_data = str(data).rstrip("\n").rstrip("\n")
		if len(self._string_data) > 0:
			try:
				d = self._string_data.split("\n")
			except ValueError:
				d = self._string_data
			while True: #Remove duplicate newlines
				try:
					d.remove("")
				except ValueError:
					break
			for i in range(len(d)):
				q = d[i]
				if q.startswith("#"):
					if "=" in q:
						self._data[q.split("=")[0]] = True
					else:
						self._data[q] = True
				else:
					if "=" in q:
						self._data[q.split("=")[0]] = str(q.split("=")[1])
					else:
						pass
				
	def _write(self, dt: str, _value = None): #Maybe implement multi-line processing
		dt = super()._unify(dt)
		
		if dt.startswith("#"):
			if "=" not in dt:
				self._data[dt] = bool(_value)
			else:
				spl = dt.split("=")
				if "true" == spl[1].lower():
					self._data[spl[0]] = True
				elif "false" == spl[1].lower():
					self._data[spl[0]] = False
				else:
					pass
		else:
			if _value is not None:
				_value = str(_value).rstrip().lstrip().rstrip("\n").lstrip("\n")
				if "=" not in dt:
					self._data[dt] = str(_value)
				else:
					self._data[dt.split("=")[0]] = str(dt.split("=")[1])
					
	def _read(self, dt: str):
		return self._data.get(super()._unify(dt), None)
	
	def _extract(self):
		data = []
		for key in list(self._data.keys()):
			if str(key).startswith("#"):
				if self._read(key):
					data += key
			else:
				data += key + "=" + self._read(key)
		d = "\n".join(data)
		if not d.endswith("\n"):
			d += "\n"
		return d
	
	def commit(self):
		data = self._extract()
		with open(super()._ensure_file(self._own_path), "r+") as f:
			super()._clear_file(self._own_path)
			f.seek(0)
			f.write(data)
	
	def read(self, key, *, requireNonNull = False):
		return self._read(key) if not requireNonNull else ""
	
	def read_flag(self, flag: str):
		if not flag.startswith("#"):
			flag = "#" + flag
		v = self._read(flag)
		return v if v is not None else False
	
	def write(self, key, value, safe = False):
		if not (safe and self._read(key) is not None):
			self._write(key, value)
			
	def write_flag(self, flag: str, value: bool):
		if not flag.startswith("#"):
			flag = "#" + flag
		self._write(flag, value)
		
class Cfg(ShadowFile):
	def __init__(self, config_name = "ADB_Tools", config_path = os.getcwd()):
		if not config_name.endswith(".cfg"):
			config_name += ".cfg"
		super().__init__(os.path.join(config_path, config_name))
		
	#TODO: Add disk update scheduling for reading and writing(one phase reads, another phase writes)