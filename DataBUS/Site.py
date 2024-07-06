from .Geog import Geog

class Site:
    description = "Site object in Neotoma"
    def __init__(self, siteid, sitename, altitude,
                 area, sitedescription, notes, geog):
        if not isinstance(siteid, (int, None)):
            raise TypeError("Site ID must be an integer or None.")
        self.siteid = siteid

        if sitename is None:
            raise ValueError(f"Sitename must be given.")
        if not isinstance(sitename, str):
            raise TypeError(f"Sitename must be a string.")
        self.sitename = sitename

        if not (isinstance(altitude, (int,float)) or altitude is None):
            raise TypeError("Altitude must be a number or None.")
        self.altitude = altitude

        if not (isinstance(area, (int, float)) or area is None):
            raise TypeError("Area must be a number or None.")
        self.area = area

        if not(isinstance(sitedescription, str) or sitedescription is None):
            raise TypeError("Site Description must be a str or None.")
        self.sitedescription = sitedescription
        
        if not(isinstance(notes, str) or notes is None):
            raise TypeError("Notes must be a str or None.")        
        self.notes = notes
        
        if not(isinstance(geog, Geog) or geog is None):
            raise TypeError("geog must be Geog or None.")
        self.geog = geog

    def __str__(self):
        return(f"{self.sitename} is located in {self.ew, self.ns}")
    
    def __eq__(self, other):
        return (self.siteid == other.siteid and
         self.sitename == other.sitename and
         self.altitude == other.altitude and
         self.area == other.area and
         self.sitedescription == other.sitedescription and
         self.notes == other.notes and
         self.geog == other.geog)

    def insert_to_db(self, cur):
        site_query = """SELECT ts.insertsite(_sitename := %(sitename)s, 
                        _altitude := %(altitude)s,
                        _area := %(area)s,
                        _descript := %(description)s,
                        _notes := %(notes)s,
                        _east := %(ew)s,
                        _north := %(ns)s,
                        _west := %(ew)s,
                        _south := %(ns)s)"""
        inputs = {'siteid': self.siteid,
                  'sitename': self.sitename,
                  'altitude': self.altitude,
                  'area': self.area,
                  'sitedescription': self.sitedescription,
                  'notes': self.notes,
                  'ew': self.geog.lat,
                  'ns':  self.geog.long}
        cur.execute(site_query, inputs)
        self.siteid = cur.fetchone()[0]
        return self.siteid
        
    def upsert_to_db(self, cur):
        site_query = """SELECT upsert_site(_siteid := %(siteid)s,
                                    _sitename := %(sitename)s,
                                    _altitude := %(altitude)s,
                                    _area := %(area)s,
                                    _descript := %(sitedescription)s,
                                    _notes := %(notes)s,
                                    _east := %(ew)s,
                                    _north:= %(ns)s)
                                    """
        inputs = {'siteid': self.siteid,
                'sitename': self.sitename,
                'altitude': self.altitude,
                'area': self.area,
                'sitedescription': self.sitedescription,
                'notes': self.notes,
                'ew': self.geog.lat,
                'ns': self.geog.long}
        cur.execute(site_query, inputs)
        self.siteid = cur.fetchone()[0]
        return self.siteid