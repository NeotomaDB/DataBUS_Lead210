"""
Data uncertainty structure is as follows:
CREATE TABLE IF NOT EXISTS ndb.datauncertainties (
dataid INTEGER REFERENCES ndb.data(dataid),
uncertaintyvalue float,
uncertaintyunitid integer REFERENCES ndb.variableunits(variableunitsid), uncertaintybasisid integer REFERENCES ndb.uncertaintybases(uncertaintybasisid), notes text,
CONSTRAINT uniqueentryvalue UNIQUE (dataid, uncertaintyunitid, uncertaintybasisid)
"""

class DataUncertainty:
    def __init__(self, dataid, uncertaintyvalue, uncertaintyunitid, uncertaintybasisid, notes):
        self.dataid = dataid
        self.uncertaintyvalue = uncertaintyvalue
        self.uncertaintyunitid = uncertaintyunitid # same as ndb.variableunits(variableunitsid)
        self.uncertaintybasisid = uncertaintybasisid # same as ndb.uncertaintybases(uncertaintybasisid)
        self.notes = notes

    def insert_to_db(self, cur):
        dat_un_q = """
                 SELECT ts.insertdata(_dataid := %(dataid)s,
                                      _uncertaintyvalue := %(uncertaintyvalue)s,
                                      _uncertaintyunitid := %(uncertaintyunitid)s,
                                      _uncertaintybasisid := %(uncertaintybasisid)s
                                      _notes := %(notes)s)
                 """
        inputs ={'dataid': self.dataid,
                'uncertaintyvalue': self.uncertaintyvalue,
                'uncertaintyunitid': self.uncertaintyunitid,
                'uncertaintybasisid': self.uncertaintybasisid,
                'notes': self.notes}
        print(inputs)
        cur.execute(dat_un_q, inputs)
        self.datumid = cur.fetchone()[0]
        return self.datumid
    
    def __str__(self):
        pass