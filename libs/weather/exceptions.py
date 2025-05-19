
class WeatherBaseException(Exception):
    """
    General Weather Exception
    """
    pass

class WeatherPermissionException(WeatherBaseException):
    """
    For errors caused by permission issues
    """
    pass