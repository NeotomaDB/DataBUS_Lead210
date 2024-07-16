with open('./DataBUS/sqlHelpers/insert_pb_model.sql', 'r') as sql_file:
    insert_pb_model = sql_file.read()

class LeadModel:
    def __init__(self, pbbasisid = None, analysisunitid = None, cumulativeinventory = None):
        self.pbbasisid = pbbasisid
        self.analysisunitid = analysisunitid
        self.cumulativeinventory = cumulativeinventory

    def insert_to_db(self, cur):
        cur.execute(insert_pb_model)
        lead_q = """SELECT insert_lead_model(_pbbasisid := %(pbbasisid)s,
                                              _analysisunitid := %(analysisunitid)s,
                                              _cumulativeinventory := %(cumulativeinventory)s)"""
        inputs = {'pbbasisid': self.pbbasisid,
                  'analysisunitid': self.analysisunitid,
                  'cumulativeinventory': self.cumulativeinventory}

        cur.execute(lead_q, inputs)
        return 
    
    def __str__(self):
        pass