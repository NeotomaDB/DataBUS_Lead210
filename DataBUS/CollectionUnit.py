from .Geog import Geog, WrongCoordinates

class CollectionUnit:
    description = "Collection Unit object in Neotoma"
    def __init__(self, handle, core, colltypeid, depenvtid, collunitname, colldate, colldevice,
                 gpsaltitude, gpserror, waterdepth, substrateid, slopeaspect, slopeangle, 
                 location, notes, geog):
        if isinstance(handle, list) and len(handle) > 1:
            raise ValueError('✗ There can only be a single collection unit handle defined.')
        handle = None if handle == ['NA'] else handle
        self.handle = handle
        if self.handle is None:
            self.handle = core[:10] #if handle is none, use core to defind handle
        self.colltypeid = colltypeid
        self.depenvtid = depenvtid
        self.collunitname = collunitname
        self.colldate = colldate
        self.colldevice = colldevice
        self.gpsaltitude = gpsaltitude
        self.gpserror = gpserror
        self.waterdepth = waterdepth
        self.substrateid = substrateid
        self.slopeaspect = slopeaspect
        self.slopeangle = slopeangle
        self.location = location
        self.notes = notes
        if not(isinstance(geog, Geog) or geog is None):
            raise TypeError("geog must be Geog or None.")
        self.geog = geog
        self.distance = None
    
    def __str__(self):
        statement = (f"Name: {self.collunitname}, "
               f"Handle: {self.handle}, "
               f"Geog: {self.geog}")
        if self.distance is None:
            return statement
        else:
            return statement + f", Distance: {self.distance:<10}" 
    
    def find_close_collunits(self, cur, distance = 10000, limit = 10):
        close_handles = """
                SELECT st.*, cu.handle,
                    ST_SetSRID(ST_Centroid(st.geog::geometry), 4326)::geography <-> ST_SetSRID(ST_Point(%(long)s, %(lat)s), 4326)::geography AS dist
                FROM   ndb.sites AS st
                INNER JOIN ndb.collectionunits AS cu ON cu.siteid = st.siteid
                WHERE ST_SetSRID(ST_Centroid(st.geog::geometry), 4326)::geography <-> ST_SetSRID(ST_Point(%(long)s, %(lat)s), 4326)::geography < %(distance)s
                ORDER BY dist
                LIMIT %(lim)s;"""
        cur.execute(close_handles, {'long': self.geog.longitude, 'lat':self.geog.latitude, 'distance': distance, 'lim': limit})
        close_handles = cur.fetchall()
        return close_handles