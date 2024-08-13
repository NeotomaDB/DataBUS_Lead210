class Publication:
    description = "Site object in Neotoma"

    def __init__(
        self,
        pubtypeid = None, # Placeholder
        year = None,
        citation = None,
        title = None,
        journal = None,
        vol = None,
        issue = None,
        pages = None,
        citnumber = None,
        doi = None,
        booktitle = None,
        numvol = None,
        edition = None,
        voltitle = None,
        sertitle = None,
        servol = None,
        publisher = None,
        url = None,
        city = None,
        state = None,
        country = None,
        origlang = None,
        notes = None):

        self.publicationid = None
        self.pubtypeid = pubtypeid
        self.year = year
        self.citation = citation
        self.title = title
        self.journal = journal
        self.vol = vol
        self.issue = issue
        self.pages = pages
        self.citnumber = citnumber
        self.doi = doi
        self.booktitle = booktitle
        self.numvol = numvol
        self.edition = edition
        self.voltitle = voltitle
        self.sertitle = sertitle
        self.servol = servol
        self.publisher = publisher
        self.url = url
        self.city = city
        self.state = state
        self.country = country
        self.origlang = origlang
        self.notes = notes

    def insert_to_db(self, cur):
        """
     
        """
        publication_query = """SELECT ts.insertpublication(
                        _pubtypeid := %(pubtypeid)s,
                        _year := %(year)s,
                        _citation := %(citation)s,
                        _title := %(title)s,
                        _journal := %(journal)s,
                        _vol := %(vol)s,
                        _issue := %(issue)s,
                        _pages := %(pages)s,
                        _citnumber := %(citnumber)s,
                        _doi := %(doi)s,
                        _booktitle := %(booktitle)s,
                        _numvol := %(numvol)s,
                        _edition := %(edition)s,
                        _voltitle := %(voltitle)s,
                        _sertitle := %(sertitle)s,
                        _servol := %(servol)s,
                        _publisher := %(publisher)s,
                        _url := %(url)s,
                        _city := %(city)s,
                        _state := %(state)s,
                        _country := %(country)s,
                        _origlang := %(origlang)s,
                        _notes := %(notes)s)"""
        inputs = {
            "pubtypeid": self.pubtypeid,
            "year": self.year,
            "citation": self.citation,
            "title": self.title,
            "journal": self.journal,
            "vol": self.vol,
            "issue": self.issue,
            "pages": self.pages,
            "citnumber": self.citnumber,
            "doi": self.doi,
            "booktitle": self.booktitle,
            "numvol": self.numvol,
            "edition": self.edition,
            "voltitle": self.voltitle,
            "sertitle": self.sertitle,
            "servol": self.servol,
            "publisher": self.publisher,
            "url": self.url,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "origlang": self.origlang,
            "notes": self.notes
        }
        cur.execute(publication_query, inputs)
        self.publicationid = cur.fetchone()[0]
        return self.publicationid