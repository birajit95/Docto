import logging


class CustomLogger:
    @staticmethod
    def set_up_logger(logger_name, log_file, level, format):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter(format)
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)


