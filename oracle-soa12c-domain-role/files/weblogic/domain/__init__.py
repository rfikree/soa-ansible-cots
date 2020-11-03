from java.util.logging import Level, Logger
import inspect
import re
import sys
import os
from com.oracle.cie.domain.script.jython import WLSTException

# Global variable for WLST commands
wlst = {}

class LogHelper:
    def __init__(self, source_class):
        self._logger = Logger.getLogger(source_class)
        self.source_class = source_class
        self._setup_logger()

    class _LogOutInfo:
        _logger = None

        def __init__ (self, logger):
            self._logger = logger

        def write(self, msg):
            method_name = inspect.stack()[1][3]
            self._logger.logp(Level.INFO, 'stdout', method_name, msg)

    class _LogOutErr:
        _logger = None

        def __init__ (self, logger):
            self._logger = logger

        def write(self, msg):
            if len(inspect.stack()) >= 3:
                method_name = [1][3]
            else:
                method_name = ''
            self._logger.logp(Level.SEVERE, 'stderr', method_name, msg)

    def _message(self, log_message):
        regex=r'\v'
        return re.sub(regex, '', log_message, 0, re.MULTILINE)

    def _setup_logger(self):
        sys.stdout = self._LogOutInfo(self._logger)
        sys.stderr = self._LogOutErr(self._logger)

    def _get_calling_method(self):
        return sys._getframe(2).f_code.co_name

    def log(self, level=Level.INFO, message='test'):
        method=self._get_calling_method()
        self._logger.logp(level, self.source_class, method, message)

    def info(self, message):
        method=self._get_calling_method()
        self._logger.logp(Level.INFO, self.source_class, method, message)

    def warn(self, message):
        method=self._get_calling_method()
        self._logger.logp(Level.WARNING, self.source_class, method, message)

    def error(self, message):
        method=self._get_calling_method()
        self._logger.logp(Level.SEVERE, self.source_class, method, message)

def validate_directory(dir_name, create=False):
    directory = os.path.realpath(dir_name)
    if not os.path.exists(directory):
        if create:
            os.makedirs(directory)
        else:
            message = 'Directory ' + directory + ' does not exist'
            raise WLSTException(message)
    elif not os.path.isdir(directory):
        message = 'Path %s is not a directory' % directory
        raise WLSTException(message)
    return fix_path(directory)

def fix_path(path):
    result = path
    if path is not None:
        result = path.replace('\\', '/')
    return result
