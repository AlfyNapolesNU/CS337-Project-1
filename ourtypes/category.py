from ourtypes.contender import Contender

class Category:

    def __init__(self, type):
        #k: contender name: lower case, no spaces
        #v: object of class Contender
        self.contenders = {}
        possible_types = ("hosts", "nominees", "presenters", "winners")
        assert type in possible_types
        self.type = type
    

    def __add(self, name, name_list, name_key):
        #we can delete later but just for checks
        assert name == name.lower().strip(), "name should be lowercase!"
        assert len(name_list) >= 2, "need at least first and last name"
        assert name_key == name.replace(" ",""), "incorrect syntax for key, no spaces!"
        assert self.contenders.get(name_key) == None, "should NOT be in dict already"

        #ok you are good, add to dict
        contender = Contender(name)
        self.contenders[name_key] = contender

        return contender

    def __handleOneName(self, name):
        """
        Only enter if name passed originally has no whitespace
        & is not in dict already, 
        maybe just first name or last name or nickname?
        i.e. Leo for Leonardo Decaprio
        """
        for k in self.contenders.keys():
            if name in k:
                #ok so some partial matching here, let's tenatively vote
                contender = self.contenders.get(k)
                #this better pass
                assert isinstance(contender, Contender)
                #yay! just update it 
                contender.maybeVoteForMe()
                return True, contender
        return False, None

    def vote_contender(self, name, cocontender=None):
        """ Public method 
        - takes a contender name as a string & checks for contender name in dictionary of contenders
        - adds new contender to dict with 1 vote OR increments number votes
        - handle only first name, last name or name not seperated? nicknames?
        - success code?
        """
        assert isinstance(name, str)
        #name key for dict - lowercase, no spaces
        name_key = name.replace(" ", "")
        
        if cocontender is not None:
            assert self.type != "winners"
            cocontenderExist = True
            cocontender=cocontender.replace(" ","")

        else:
            cocontenderExist = False

        #first thing we will check is if it is already in our dict
        contender = self.contenders.get(name_key)
        if contender is not None:
            #this better pass
            assert isinstance(contender, Contender)
            #yay! just update it 
            contender.voteForMe()
            if cocontenderExist:
                contender.voteCoContender(cocontender)
            return #done

        #hmmm... it is not in our dict
        #let's check validity of name: FirstName LastName ... 
        name_list = name.split(" ")

        match len(name_list):
            case 1:
                #only first or last name since key has no whitespace
                assert name == name_key, "just a check"
                found, contender = self.__handleOneName(name)
                if cocontenderExist & found:
                    contender.voteCoContender(cocontender)
                return
            case 2:
                #formatted correctly, add to dict
                contender = self.__add(name, name_list, name_key)
                if cocontenderExist:
                    contender.voteCoContender(cocontender)
                return #done
            case _:
                #here we would want to check for incorrect parsing if names aren't two words
                return
    

    def total_votes(self):
        """Return list sorted by vote counts
        type --> [(name, votes), (name, votes) ...] in descending order
        """
        
        vote_counter = [(ele[1].name, ele[1].voteCount(), ele[1].getTopCoContender()) for ele in self.contenders.items()]
        vote_counter = sorted(vote_counter, key=lambda x: x[1], reverse=True)
        return vote_counter

    def __str__(self):
        return "\n".join([str(x) for x in self.contenders.values()])
        

