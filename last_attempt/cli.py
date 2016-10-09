"""
last_attempt
 
Usage:
  last_attempt runserver [--portnumber <number>]
  last_attempt data --outfile <filename> 
  last_attempt model run-tests --infile <filename>
  last_attempt model train --infile <filename> --clf <type>
  last_attempt model run --infile <filename>
  last_attempt listfiles
  last_attempt -h | --help
  last_attempt --version
 
Options:
  -h --help                               Show this screen.
  -v --version                            Show version.
  -p <number> --portnumber <number>       OpenBCI Dongle Port.
  -o <file> --outfile <file>              Absolute path to outfile.
  -i <file> --infile <file>               Absolute path to outfile.
  --clf <type>                            Classifier type.

Help:
  For help using this tool, please open an issue on the Github repository:
  
"""

from inspect import getmembers, isclass
from docopt import docopt
__version__ = "0.0.1"

def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=__version__)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k):
            if v == True:
                module = getattr(commands, k)
                commands = getmembers(module, isclass)
                command = [cmd_class for cmd_name,cmd_class in commands if cmd_name == k.title()][0]
                command = command(options)
                command.run()