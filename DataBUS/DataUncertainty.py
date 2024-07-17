with open('./DataBUS/sqlHelpers/insert_data_uncertainty.sql', 'r') as sql_file:
    insert_data_uncertainty = sql_file.read()

class DataUncertainty:
    def __init__(self, dataid, uncertaintyvalue, uncertaintyunitid, uncertaintybasisid, notes):
        self.dataid = dataid
        if uncertaintyvalue == 'NA':
            uncertaintyvalue = None
        self.uncertaintyvalue = uncertaintyvalue
        if uncertaintyunitid == 'NA':
            uncertaintyunitid = None
        self.uncertaintyunitid = uncertaintyunitid # same as ndb.variableunits(variableunitsid)
        if uncertaintybasisid == 'NA':
            uncertaintybasisid = None
        self.uncertaintybasisid = uncertaintybasisid # same as ndb.uncertaintybases(uncertaintybasisid)
        self.notes = notes

    def insert_to_db(self, cur):
        cur.execute(insert_data_uncertainty)
        dat_un_q = """
                 SELECT insert_data_uncertainty(_dataid := %(dataid)s,
                                                   _uncertaintyvalue := %(uncertaintyvalue)s,
                                                   _uncertaintyunitid := %(uncertaintyunitid)s,
                                                   _uncertaintybasisid := %(uncertaintybasisid)s,
                                                   _notes := %(notes)s)
                 """
        inputs ={'dataid': self.dataid,
                'uncertaintyvalue': self.uncertaintyvalue,
                'uncertaintyunitid': self.uncertaintyunitid,
                'uncertaintybasisid': self.uncertaintybasisid,
                'notes': self.notes}
        cur.execute(dat_un_q, inputs)
        return 
    
    def __str__(self):
        pass