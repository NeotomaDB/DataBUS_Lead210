class Response:
    def __init__(self, valid = [], message = []):
        self.valid = valid
        self.message = message
        self.validAll = None
    
    def __str__(self):
        return(f"Valid: {self.validAll} \n"
               f"Message: \n"
               f"{self.message}")

class SiteResponse(Response):
    def __init__(self):
        super().__init__()
        self.matched = {'namematch': False, 'distmatch': False}
        self.doublematched = (self.matched['namematch'] and self.matched['distmatch'])
        self.sitelist = []
        self.closesites = []
    
    def __str__(self):
        response_str = super().__str__()
        response_str += f"\n Matched: {self.doublematched}"
        if self.closesites:
            response_str += f"\n Close Sites: {self.closesites}"
        if self.sitelist:
            response_str += f"\n Sitelist: {self.sitelist}"
        return response_str