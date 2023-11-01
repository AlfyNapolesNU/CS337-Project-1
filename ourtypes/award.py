from ourtypes.category import Category

class Award:
    """
    We need some type constaints here
    need to get
    - presenters 
    - nominees
    - winners
    
    Types
    each is a Category object
    k = lowercasename no spaces
    v = object of type Person

    winner_type = Person or Thing (movie, tv show, etc.)
    voting is handled for you buy the category, contender types
    """
    
    

    def __init__(self, award_name, winner_type=None):
        #dictionaries to store nominees, winners, presenters
        self.nominees = Category(type="nominees")
        self.winners = Category(type="winners")
        self.presenters = Category(type="presenters")
        
        #award name
        self.award_name = award_name
        self.winner_type = winner_type
        self.aliases = []

    def check_name(self, name):
        if self.winner_type == "Thing":
            possible_names = 

    def add_alias(self, aliases):
        aliases = [a.replace("  ", " ") for a in aliases]
        self.aliases += aliases

    def add_winner(self, winner):
        if winner != " ":
            self.winners.vote_contender(winner)
    

    def add_nominee(self, nominee, cocontenders=None):
        if nominee != " ":
            self.nominees.vote_contender(nominee)
        #handle cocontenders


    def add_presenter(self, presenter, cocontenders=None):
        if presenter != " ":
            self.presenters.vote_contender(presenter)
        #handle cocontender

    def __str__(self):
        return f"Award: {self.award_name}\nNominees: {self.nominees}\nWinners: {self.winners.get_winner()}\nPresenters: {self.presenters.get_winner()}\n"
        

        

