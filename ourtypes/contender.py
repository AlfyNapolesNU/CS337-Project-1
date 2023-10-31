class Contender:
    """this could be a winner, host, or nominee, presenter
    Fields:
        - name: str
        - name_list: list of str, length >= 2
        - votes: default to 1 
            - if unsure use 0.5 as vote
    """

    def __init__(self, name):
        #check its a string
        assert isinstance(name, str), "name is not type str"
        #don't want to do this twice
        assert name == name.strip().lower(), "strip and lowercase name pls!"

        #split by whitespace
        name_list = [x for x in name.split(" ")]

        #check we have first and last name 
        assert len(name_list) >= 2, "pls format name as firstName lastName ..."

        self.name = name
        self.name_list = name_list
        self.votes = 1
        self.name_key = "".join(self.name_list)
        self.cocontenders = {}

    def voteCoContender(self, cocontender):
        assert isinstance(cocontender, str)
        self.cocontenders[cocontender] = self.cocontenders.get(cocontender, 0) + 1
    
    def getTopCoContender(self):
        if len(self.cocontenders)==0:
            return None
        else:
            sortedcocontenders = sorted(self.cocontenders.items(), key=lambda item: item[1], reverse=True)
            return sortedcocontenders[0]

    #increment vote count
    def voteForMe(self):
        self.votes += 1

    def maybeVoteForMe(self):
        self.votes += 0.5

    def voteCount(self):
        return self.votes
    
    #define a generator for this class
    def iterContender(self):
        i = 0
        while i < len(self.name_list):
            yield self.name_list[i]
            i += 1
    
    #returns the name with no spaces, lowercase
    def nameNoSpaces(self):
        return self.name_key
    
    def typeCheck(self):
        return "Not Implemented"
    
    def __str__(self):
        if len(self.cocontenders) == 0:
            return f'Name: {self.name}, Votes: {self.votes}'
        else:
            ch = self.getTopCoContender()
            return f'Name: {self.name}, Votes: {self.votes}, cocontender: {ch[0]}, cocontender Votes: {ch[1]}'
            