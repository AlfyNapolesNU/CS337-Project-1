from ourtypes.category import Category
import itertools

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
        with open("100CommonWords.txt", 'r') as file:
            self.common_english_words = set(file.read().splitlines())

    def check_name(self, name):
        l = []
        if self.winner_type == "Thing":
            possible_names = name.split(" ")
            if len(possible_names) > 1: 
                for i, j in itertools.combinations(range(len(possible_names) + 1), 2):
                    l.append(" ".join(possible_names[i:j]))
        return l

    def add_alias(self, aliases):
        aliases = [a.replace("  ", " ") for a in aliases]
        self.aliases += aliases

    def add_winner(self, winner):
        winner = winner.lower()
        if winner.isspace():
            return
        self.winners.vote_contender(winner)
        possible_names = self.check_name(winner)
        for name in possible_names:
            self.winners.vote_contender(name)
                
    

    def add_nominee(self, nominee, cocontenders=None):
        nominee = nominee.lower()
        if nominee.isspace():
            return
        self.nominees.vote_contender(nominee)
        possible_names = self.check_name(nominee)
        for name in possible_names:
            self.nominees.vote_contender(name)
        #handle cocontenders


    def add_presenter(self, presenter, cocontender=None):
        presenter = presenter.lower()
        if presenter.isspace():
            return
        if cocontender is not None:
            self.presenters.vote_contender(presenter, cocontender)
        else:
            self.presenters.vote_contender(presenter)
        #handle cocontender


    def get_top_nominees(self):
        vc = self.nominees.total_votes()
        out = []
        if vc == []:
            return ""
        else:
            for ele in vc:
                if "won" in ele[0] or "win" in ele[0] or "golden globe" in ele[0]:
                    continue
                if len(out) == 4: break
                if self.winner_type == "Person":
                    if len(ele[0].split(" ")) == 2:
                        out.append(ele[0])
                else:
                    out.append(ele[0])
        f = ""
        for ele in out:
            f += str(ele) + ", "
        return f


    def get_presenters(self):
        vc = self.presenters.total_votes()
        if vc == []:
            return ""
        else:
            top = vc[0]
            if top[2] is not None:
                cohost = top[2][0]
                if len(vc) > 2:
                    possible_cohosts = [ele[0] for ele in vc]
                else:
                    possible_cohosts = [ele[0] for ele in vc]
                for ch in possible_cohosts:
                    if ch.replace(" ", "") == cohost:
                        return str(top[0]) + ", " + str(ch)
            elif top is not None:
                return str(top[0])
        
    def __str__(self):
        return f"Award: {self.award_name}\nPresenters: {self.get_presenters()}\nNominees: {self.get_top_nominees()}\nWinner: {self.winners.get_winner()}\n"
        

        

