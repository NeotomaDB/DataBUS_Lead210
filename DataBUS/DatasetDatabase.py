class DatasetDatabase:
    def __init__(self, databaseid, datasetid = None):
        if isinstance(datasetid, int) or datasetid is None:
           self.datasetid = datasetid
        else:
            raise ValueError("Dataset ID must be an integer.")
        self.datasetid = datasetid
        if isinstance(databaseid, int) or databaseid is None:
           self.repositoryid = databaseid 
 
    def insert_to_db(self, cur):
        db_query = """
               SELECT ts.insertdatasetdatabase(_datasetid := %(datasetid)s, 
                                               _databaseid := %(databaseid)s)
               """
        inputs = {'datasetid': self.datasetid,
                  'databaseid': self.databaseid}
        print(inputs)
        cur.execute(db_query, inputs)
        return

    def __str__(self):
        pass