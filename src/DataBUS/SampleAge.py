class SampleAge:
    def __init__(
        self, sampleid=None, chronologyid=None, age=None, ageyounger=None, ageolder=None
    ):
        self.sampleid = sampleid
        self.chronologyid = chronologyid
        self.age = age
        self.ageyounger = ageyounger
        self.ageolder = ageolder

    def insert_to_db(self, cur):
        sample_q = """
        SELECT ts.insertsampleage(_sampleid := %(sampleid)s, 
                                  _chronologyid := %(chronologyid)s, 
                                  _age := %(age)s, 
                                  _ageyounger := %(ageyounger)s, 
                                  _ageolder := %(ageolder)s)
                        """
        inputs = {
            "sampleid": self.sampleid,
            "chronologyid": self.chronologyid,
            "age": self.age,
            "ageyounger": self.ageyounger,
            "ageolder": self.ageolder,
        }

        cur.execute(sample_q, inputs)
        self.sampleage = cur.fetchone()[0]
        return self.sampleage

    def __str__(self):
        pass
