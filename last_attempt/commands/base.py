# last-attempt/commands/base.py
"""The base command."""
import os
from ConfigParser import SafeConfigParser
 
class Base(object):
	"""A base command."""
 
	def __init__(self, options, *args, **kwargs):
		self.options = options
		self.args = args
		self.kwargs = kwargs
		self.config = self.load_config()
		self.env_path = os.environ[self.config.get('general', 'ENV')]
 
	def run(self):
		raise NotImplementedError('You must implement the run() method yourself!')

	def load_config(self):
		config = SafeConfigParser()
		config.read(os.path.dirname(os.path.abspath(__file__)) + "/../config.ini")

		env_path = os.environ[config.get('general','ENV')]
		try:
			local_config = ConfigParser.ConfigParser()
			local_config.read(env_path + "local_config.ini")
			config = local_config
		except:
			with open(env_path + "local_config.ini",'w') as cfgfile:
				config.write(cfgfile)

		return config
