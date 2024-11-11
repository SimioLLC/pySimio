from pysimio.logger import logger
from http_exceptions import UnauthorizedException

class AuthenticationError(Exception):
    pass

def exception_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except AuthenticationError as e:
            logger.fatal(f"An error occurred, please try again later. {e}")
        return wrapper