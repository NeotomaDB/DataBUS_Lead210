class WrongCoordinates(Exception):
    pass

class Geog:
    def __init__(self, lat, long):
        if not(isinstance(lat, (int, float)) or lat is None):
            raise TypeError("Latitude must be a number or None.")
        if not(isinstance(long, (int, float)) or long is None):
            raise TypeError("Longitude must be a number or None.")
        if isinstance(lat, (int,float)) and not(-90 <= lat <= 90):
            raise WrongCoordinates("Latitude must be between -90 and 90.")
        if  isinstance(long, (int,float)) and not(-180 <= long <= 180):
            raise WrongCoordinates("Longitude must be between -180 and 180.")
        self.lat = lat
        self.long = long
        
    def __str__(self):
        return(f"Point({self.lat=}, {self.long=})")