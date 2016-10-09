#!/usr/bin/python

# skele/commands/runserver.py
'''
The runserver command.
---------------

This is the main module for establishing an OpenBCI stream through the Lab Streaming Layer (LSL).

Lab streaming layer is a networking system for real time streaming, recording, and analysis of time-series 
data. LSL can be used to connect OpenBCI to applications that can record, analyze, and manipulate the data, 
such as Matlab, NeuroPype, BCILAB, and others.

To run the program as a GUI application, enter `python openbci_lsl.py`. 

To run the program as a command line interface, enter `python openbci_lsl.py [port] --stream`. The port argument
is optional, since the program automatically detects the OpenBCI port. However, if this functionality fails, the port must be specified as an argument.

For more information, see the readme on the Github repo:

https://github.com/gabrielibagon/OpenBCI_LSL

'''

from json import dumps
import sys
import lib.streamerlsl as streamerlsl

from .base import Base


class Runserver(Base):
	"""Run a OpenBCI server instance"""

	def run(self):
		port = self.config.get('openbci', 'port')
		if port == "None":
			port = self.options['--portnumber']
			if port == None:
				print "Please either set a portnumber in the options or the config file"
				return
		lsl = streamerlsl.StreamerLSL(port=port,GUI=False)
		lsl.create_lsl()
		lsl.begin()