
RED = "\03[91m"
YELLOW = "\33[33m"
BLUE = "\33[34m"

class Logger:
    @staticmethod
    def warn(msg: str):
        Logger.message("WARNING", YELLOW, msg)

    @staticmethod
    def error(msg: str):
        Logger.message("ERROR", RED, msg)

    @staticmethod
    def info(msg: str):
        Logger.message("INFO", BLUE, msg)

    @staticmethod
    def message(tag: str, color: str, msg: str):
        print("[{0}{1}] {2}".format(tag, color, msg))