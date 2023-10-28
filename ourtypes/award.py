import nominee, host

class Award:
    """
    We need some type constaints here
    need to get
    - presenters 
    - nominees
    - winners
    
    Types
    each is a dict
    k = lowercasename no spaces
    v = object of type Person

    winner_type = Person or Thing (movie, tv show, etc.)
    """
    


    def __init__(self, award_name, winner_type=None):
        #dictionaries to store nominees, winners, presenters
        self.nominees, self.winners, self.presenters = {}, {}, {}
        
        #award name
        self.award_name = award_name
        self.winner_type = winner_type

    def add_winner(self, winner):
        self.winner = winner.name
    
    def add_host(self, host):
        self.host = host.name

    def add_nominee(self, nominee):
        if type(nominee) == "str":
            self.nominees.append(nominee)
        else:
            for ele in nominee:
                self.nominees.append(ele)

    def add_presenter(self, presenter):
        self.presenter = presenter

