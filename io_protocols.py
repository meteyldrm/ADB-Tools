import time
import os
import sys
import uuid

class Utilities:
	@staticmethod
	def _unify(string):
		string = string.replace("\n", "")
		if string.startswith("#"):
			return "#" + string.lstrip("#").lstrip().rstrip()
		elif "=" in string:
			return "=".join([a.lstrip().rstrip() for a in string.split("=")])
	
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
	
	def _check_dir(self, _path):
		_path = self._resolve(_path)
		return os.path.exists(_path) and os.path.isdir(_path)
	
	def _ensure_dir(self, _path):
		_path = self._resolve(_path)
		if not self._check_dir(_path):
			os.mkdir(_path)
		return _path

class ShadowFile:
	data = {}
	
	def __init__(self, data: None):
		if data is not None:
			data = str(data).lstrip("\n")
			d = data.split("\n")
			
			try:
				d.remove("")
			except ValueError:
				pass
			for i in range(len(d)):
				q = d[i]
				if q.startswith("#"):
					if "=" in q:
						self.data[q.split("=")[0]] = True
					else:
						self.data[q] = True
				else:
					if "=" in q:
						self.data[q.split("=")[0]] = str(q.split("=")[1])
					else:
						pass
				
	def _write(self, dt: str, *, _value = None, _flag = True): #Maybe implement multi-line processing
		dt = dt.rstrip("\n").lstrip("\n")
		
		if dt.startswith("#"):
			if "=" not in dt:
				self.data[dt] = str(_flag)
			else:
				spl = dt.split("=")
				if "true" == spl[1].lower():
					self.data[spl[0]] = True
				elif "false" == spl[1].lower():
					self.data[spl[0]] = False
				else:
					pass
		else:
			if _value is not None:
				_value = str(_value).rstrip().lstrip().rstrip("\n").lstrip("\n")
				if "=" not in dt:
					self.data[dt] = str(_value)
				else:
					self.data[dt.split("=")[0]] = str(dt.split("=")[1])
	
class BufferManager(Utilities):
	def __init__(self, init_path):
		super().__init__()
		self.path = self._ensure_dir(self._resolve(init_path))