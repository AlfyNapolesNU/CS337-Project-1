class Person:
    """this could be a winner, host, or nominee
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

    #increment vote count
    def voteForMe(self):
        self.votes += 1

    def maybeVoteForMe(self):
        self.votes += 0.5

    def voteCount(self):
        return self.votes
    
    #define a generator for this class
    def iterPerson(self):
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
        #maybe change this?
        return f'Name: {self.name}, Votes: {self.votes}'