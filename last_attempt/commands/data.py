from json import dumps
import os

from lib.data_collector import DataCollector
from lib.data_preprocessor import DataPreprocessor
from lib.client import Client

from .base import Base


class Data(Base):
	"""Do stuff with training data"""
	def __init__(self, *args, **kwargs):
		super(Data, self).__init__(*args, **kwargs)

	def run(self):
		dc = DataCollector(self.config.getint('data', 'number-samples'),
							self.config.getint('general', 'n-gestures'))
		c = Client()
		c.read_stream(self.config.get('openbci','stream-type'), dc.data_reader)
		dp = DataPreprocessor()

		var_frame_size = self.config.getint('ml', 'var-frame-size')

		for i in range(self.config.getint('openbci','n-channels')):
			dp.running_var(dc.data_x, i, var_frame_size)

		# for i in range(self.config.getint('openbci','n-channels')):
		# 	dp.running_var(dc.data_x, i, 10)

		for i in range(self.config.getint('openbci','n-channels')):
			dp.running_var(dc.data_x, i, 20)

		for i in range(self.config.getint('openbci','n-channels')):
			dp.running_var(dc.data_x, i, 30)

		for i in range(self.config.getint('openbci','n-channels')):
			dp.running_var(dc.data_x, i, 50)

		for i in range(self.config.getint('openbci','n-channels')):
			dp.running_var(dc.data_x, i, 70)

		dc.save_data("{}.bin".format(self.env_path + "training/" + self.options['--outfile']))
