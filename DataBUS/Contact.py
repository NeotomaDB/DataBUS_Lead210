class Contact:
    pass
    def __init__(self, contactid, contactname = None, order = None):
        if isinstance(contactid, int):
           self.contactid = contactid
        else:
            raise ValueError("ContactID must be an integer.")
        self.contactname = contactname
        if isinstance(order, int) or order is None:
           self.order = order
        else:
            raise ValueError("Order must be an integer.")
        
    def insert_pi(self, cur):
        dataset_query = """
        SELECT ts.insertdataset(_collectionunitid:= %(collunitid)s,
                                _datasettypeid := %(datasettypeid)s,
                                _datasetname := %(datasetname)s,
                                _notes := %(notes)s);
                        """
        inputs = {'collunitid' : self.collectionunitid,
                  'datasettypeid': self.datasettypeid,
                  'datasetname': self.datasetname,
                  'notes': self.notes}
        print(inputs)
        cur.execute(dataset_query, inputs)
        self.datasetid = cur.fetchone()[0]
        return self.datasetid
    
    def insert_sample_analyst(self, cur):
        pass

    def insert_XX():
        pass

    def __str__(self):
        pass