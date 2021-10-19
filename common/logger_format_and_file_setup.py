import os
import logging
from DOCTO.settings import BASE_DIR
from .custom_logger import CustomLogger

def initialize_logger():
    CustomLogger.set_up_logger('log1', os.path.join(BASE_DIR, 'logs', "log1.log"), level=logging.ERROR,
                               format='%(levelname)s / %(asctime)s / %(message)s / %(pathname)s / %(funcName)s / %(lineno)d')

    CustomLogger.set_up_logger('log2', os.path.join(BASE_DIR, 'logs', "log2.log"), level=logging.WARNING,
                               format='%(levelname)s / %(asctime)s / %(message)s / %(pathname)s / %(funcName)s / %('
                                      'lineno)d')