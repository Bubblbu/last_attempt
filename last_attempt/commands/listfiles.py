from json import dumps
import time
import os
import ConfigParser

from .base import Base

class Listfiles(Base):
	"""Do stuff with training data"""

	def run(self):
		env_path = os.environ[self.config.get('general', 'ENV')]
		
		print "\n# ==== Training data ===="
		for root, _, filenames in os.walk(env_path + "training"):
			for filename in filenames:
				file_path = root + '/' + filename
				created = os.path.getctime(file_path)
				modified = os.path.getmtime(file_path)

				print "+ %s" % filename
				print "    Created:       %s" % time.ctime(created)
				print "    Last modified: %s" % time.ctime(modified)

		print "\n# ==== Trained Models ===="
		for root, _, filenames in os.walk(env_path + "models"):
			for filename in filenames:
				file_path = root + '/' + filename
				created = os.path.getctime(file_path)
				modified = os.path.getmtime(file_path)

				print "+ %s" % filename
				print "    Created:       %s" % time.ctime(created)
				print "    Last modified: %s" % time.ctime(modified)
