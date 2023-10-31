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

    def add_winner(self, winner):
        self.winners.vote_contender(winner)
        
    

    def add_nominee(self, nominee, cocontenders):
        self.nominees.vote_contender(nominee)
        #handle cocontenders


    def add_presenter(self, presenter, cocontenders):
        self.presenters.vote_contender(presenter)
        #handle cocontender
        
        

        

