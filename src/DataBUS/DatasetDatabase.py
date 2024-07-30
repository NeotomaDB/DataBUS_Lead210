class DatasetDatabase:
    def __init__(self, databaseid, datasetid=None):
        if isinstance(datasetid, int) or datasetid is None:
            self.datasetid = datasetid
        else:
            raise ValueError("Dataset ID must be an integer.")
        self.datasetid = datasetid
        if isinstance(databaseid, int) or databaseid is None:
            self.databaseid = databaseid
        else:
            raise ValueError("DatabaseID must be an integer.")

    def insert_to_db(self, cur):
        db_query = """
               SELECT ts.insertdatasetdatabase(_datasetid := %(datasetid)s, 
                                               _databaseid := %(databaseid)s)
               """
        inputs = {"datasetid": self.datasetid, "databaseid": self.databaseid}
        cur.execute(db_query, inputs)
        return

    def __str__(self):
        pass
