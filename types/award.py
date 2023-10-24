import winner, presenter, nominee, host

class Award:
    """
    We need some type constaints here
    
    """
    nominees = []

    def __init__(self, name, winner_type=None):
        self.name = name

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

