import logging

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    DEBUG = '\033[96m'
    INFO = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    EXCEPTION = ERROR + BOLD 
    UNDERLINE = '\033[4m'
    CRITICAL = EXCEPTION + UNDERLINE

class Logger:
    def __init__(self, fileName = './.logs.txt', 
                 fileformat = '%(asctime)s - %(levelname)s - %(message)s',
                 streamformat = '%(name)s - %(levelname)s - %(message)s',
                 fileLevel = logging.INFO, streamLevel = logging.WARNING):
        try :
            self.fileName = fileName
            self.format = format
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.DEBUG)

            self.fileHandler = logging.FileHandler(self.fileName)
            self.fileHandler.setLevel(fileLevel)
            self.fileHandler.setFormatter(logging.Formatter(fileformat))
            self.filLevel = fileLevel

            self.streamHandler = logging.StreamHandler()
            self.streamHandler.setLevel(streamLevel)
            self.streamHandler.setFormatter(logging.Formatter(streamformat))
            self.streamLevel = streamLevel

            self.logger.addHandler(self.streamHandler)
            self.logger.addHandler(self.fileHandler)
        
        except Exception as E :
            print(E)

    def logInfo(self, message = ""):
        try :
            if ( self.streamLevel == logging.INFO ):
                print(Colors.INFO)
            self.logger.info(message)
            if ( self.streamLevel == logging.INFO ):
                print(Colors.ENDC)

        except Exception as E :
            print(E)
    
    def logError(self, message = "" ):
        try :
            print(Colors.ERROR)
            self.logger.error(message)
            print(Colors.ENDC)

        except Exception as E :
            print(E)

    
    def logWarning(self, message = ""):
        try :
            print(Colors.WARNING)
            self.logger.warning(message)
            print(Colors.ENDC)

        except Exception as E :
            print(E)
    
    def logDebug(self, message = "" ):
        try :
            print(Colors.DEBUG)
            self.logger.debug(message)
            print(Colors.ENDC)

        except Exception as E :
            print(E)

    def logCritical(self, message = "" ):
        try :
            print(Colors.CRITICAL)
            self.logger.critical(message)
            print(Colors.ENDC)
        except Exception as E :
            print(E)

    def logException(self, message = "" ):
        try :
            print(Colors.EXCEPTION)
            self.logger.exception(message)
            print(Colors.ENDC)
        except Exception as E :
            print(E)
    
    def removeStreamHandler(self):
        self.logger.removeHandler(self.streamHandler)

    def removeFileHandler(self):
        self.logger.removeHandler(self.fileHandler)

    def addStreamHandler(self):
        self.logger.addHandler(self.streamHandler)

    def addFileHandler(self):
        self.logger.addHandler(self.fileHandler)


if __name__ == '__main__':
    thisLogger = Logger()
    thisLogger.logDebug("This is a debug message")
    thisLogger.logInfo("This is an info message")
    thisLogger.logWarning("This is a warning message")
    thisLogger.logError("This is an error message")
    thisLogger.logException("This is an exception message")
    thisLogger.logCritical("This is a critical message")
