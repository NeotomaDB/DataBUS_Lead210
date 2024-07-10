class AnalysisUnit:
    description = "Analysis Unit object in Neotoma"
    def __init__(self, analysisunitid = None, collectionunitid = None, analysisunitname = None, 
                 depth = None, thickness = None, faciesid = None, mixed = None, igsn = None, notes = None,
                 recdatecreated = None, recdatemodified = None):
        self.analysisunitid = analysisunitid #int
        self.collectionunitid = collectionunitid #int
        self.analysisunitname  = analysisunitname #str
        self.depth = depth #float
        self.thickness = thickness #float
        self.faciesid = faciesid #int
        self.mixed = mixed #bool
        self.igsn = igsn #str
        self.notes = notes #str
        self.recdatecreated = recdatecreated # date
        self.recdatemodified = recdatemodified #date
    
    def __str__(self):
        statement = (f"Name: {self.analysisunitname}, "
                     f"ID: {self.analysisunitid}, ")
        return statement
    

