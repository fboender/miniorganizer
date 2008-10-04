#!/usr/bin/python

import os

class Config(dict):
	"""
	Config class handles reading and updating configurations. Config instances
	are dicts. Configuration can be updated from both files and dictionaries.
	This config class supports marshelling of data types (int, bool, string)
	from and to configuration files, as well as default values when values are
	not specified in the configuration file.
	"""
	
	defaults = {
	}

	configfile = None

	def __init__(self, config = None, defaults = None):
		"""
		Create a new Config instance. config is either the path to .ini style
		configuration file or a dictionary with configuration key/value pairs.

		If the key exists in defaults then the value will automatically be cast
		to the correct type (int, bool, etc). If a key which exists in defaults
		isn't present in the configuration file or dictionary it will be
		initialized with a default value. Defaults can be specified like this:

		defaults = {
			'debug': (int, 30),
			'default_show': (str, 'Month'),
			'cal_show_weeknr': (bool, 1),
		}
		config = config.Config(filename, defaults)
		"""

		if defaults:
			self.defaults = defaults

		if config:
			self.update(config)

	def __setitem__(self, k, v):
		if k in self.defaults:
			type_, default = self.defaults[k]
			if type(v) != type_:
				raise ValueError('Values for key \'%s\' should be of type \'%s\', but is \'%s\'' % (k, type_, type(v)))
		dict.__setitem__(self, k, v)

	def __getitem__(self, k):
		if self.has_key(k):
			return(dict.__getitem__(self, k))
		elif k in self.defaults:
			return(self.defaults[k][1])
		else:
			return(dict.__getitem__(self, k))

	def _cast_mem(self, k, v):
		"""
		Cast a value to the correct type for use in memory according to the
		type defined in self.defaults.
		"""
		if k in self.defaults:
			type_, default = self.defaults[k]
			if type_ == bool:
				return(bool(int(v)))
			elif type_ == int:
				return(int(v))
			else:
				return(v)
		else:
			return(v)
	
	def _cast_file(self, k, v):
		"""
		Cast a value to the correct type for use on disk according to the type
		defined in self.defaults.
		"""
		if k in self.defaults:
			type_, default = self.defaults[k]
			if type_ == bool:
				return(int(v))
			elif type_ == int:
				return(int(v))
			else:
				return(v)
		else:
			return(v)

	def update(self, E):
		"""
		Update the configuration from a configuration file or dictionary.
		"""

		if type(E) == type(dict()):
			# Update from dict
			for k, v in E.iteritems():
				self.__setitem__(k, v)
		else:
			# Update from configuration file
			self.configfile = E
			f = file(E, 'r')
			for line in f:
				if line and not line.startswith('#') and '=' in line:
					k, v = [x.strip() for x in line.split('=', 1)]
					self.__setitem__(k, self._cast_mem(k, v))
			f.close()

	def save(self, filename = None):
		"""
		Save the current configuration to filename. If filename already exists,
		it will be read, and the values in the file will be replaced with the
		values in the current configuration without destroying the formatting
		in the file.
		"""
		if not filename:
			if not self.configfile:
				raise ValueError('A filename is required')
			else:
				filename = self.configfile
			
		f_in = file(filename, 'r')
		fc = []
		seen_keys = []
		for line in f_in:
			if line and not line.startswith('#') and '=' in line:
				# Line contains a configuration item. Replace the value with
				# what's in the current configuration
				k, v = [x.strip() for x in line.split('=', 1)]
				seen_keys.append(k)
				if k in self:
					# Key is set in in-memory configuration. Replace file value with memory value.
					v = self[k]
					if k in self.defaults:
						v = self._cast_file(k, v)
					fc.append('%s = %s\n' % (k, v))
				else:
					# Key is not set in in-memory configuration. Just keep file version.
					fc.append(line)
			else:
				# Line doesn't contain a configuration item. Just keep it.
				fc.append(line)

		# Add any config items which are new to the file
		for k in self.keys():
			if not k in seen_keys:
				fc.append('%s = %s\n' % (k, self._cast_file(k, self[k])))
				
		f_in.close()
		
		f_out = file(filename, 'w')
		f_out.write(''.join(fc))
		f_out.close()
