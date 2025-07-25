import logging

logger = logging.getLogger("gofer")

# errrfile_h = logging.FileHandler('file.log')
fileHandler = logging.FileHandler("Logs/logs.log")


formatter = logging.Formatter('%(name)s %(levelname)s %(message)s')

logger.addHandler(fileHandler)


fileHandler.setFormatter(formatter)


