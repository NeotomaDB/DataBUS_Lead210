class Repository:
    def __init__(self, datasetid, repositoryid, notes = None):
        if isinstance(datasetid, int):
           self.datasetid = datasetid
        else:
            raise ValueError("Dataset ID must be an integer.")
        self.datasetid = datasetid
        if isinstance(repositoryid, int) or repositoryid is None:
           self.repositoryid = repositoryid
        else:
            raise ValueError("Specimens Repository ID must be an integer or None.")
        self.notes = notes
        
 
    def insert_to_db(self, cur):
        repo_query = """
            SELECT ts.insertdatasetrepository(_datasetid := %(datasetid)s, 
                                               _repositoryid := %(repositoryid)s,
                                               _notes := %(notes)s)
                                            """
        inputs = {'datasetid': self.datasetid,
                  'repositoryid': self.repositoryid,
                  'notes': self.notes}
        cur.execute(repo_query, inputs)
        return

    def __str__(self):
        pass