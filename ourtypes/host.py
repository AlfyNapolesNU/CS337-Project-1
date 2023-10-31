from ourtypes.person import Person

class Hosts:

    def __init__(self):
        #k: host name: lower case, no spaces
        #v: object of class Person or list of Person
        self.hosts = {}
    

    def __add(self, name, name_list, name_key):
        #we can delete later but just for checks
        assert name == name.lower().strip(), "name should be lowercase!"
        assert len(name_list) >= 2, "need at least first and last name"
        assert name_key == name.replace(" ",""), "incorrect syntax for key, no spaces!"
        assert self.hosts.get(name_key) == None, "should NOT be in dict already"

        #ok you are good, add to dict
        host = Person(name)
        self.hosts[name_key] = host
        return host

    def __handleOneName(self, name):
        """
        Only enter if name passed originally has no whitespace
        & is not in dict already, 
        maybe just first name or last name or nickname?
        i.e. Leo for Leonardo Decaprio
        """
        for k in self.hosts.keys():
            if name in k:
                #ok so some partial matching here, let's tenatively vote
                host = self.hosts.get(k)
                #this better pass
                assert isinstance(host, Person)
                #yay! just update it 
                host.maybeVoteForMe()
                return #done

    def vote_host(self, name, cohost=None):
        """ Public method 
        - takes a host name as a string & checks for host name in dictionary of hosts
        - adds new host to dict with 1 vote OR increments number votes
        - handle only first name, last name or name not seperated? nicknames?
        - success code?
        """
        assert isinstance(name, str)
        #remove whitespace
        name = name.strip()
        #name key for dict - lowercase, no spaces
        name_key = name.replace(" ", "")
        
        if cohost is not None:
            cohostExist = True
            cohost=cohost.strip().replace(" ","")
        else:
            cohostExist = False

        #first thing we will check is if it is already in our dict
        host = self.hosts.get(name_key)
        if host is not None:
            #this better pass
            assert isinstance(host, Person)
            #yay! just update it 
            host.voteForMe()
            if cohostExist:
                host.voteCoHost(cohost)
            return #done

        #hmmm... it is not in our dict
        #let's check validity of name: FirstName LastName ... 
        name_list = name.split(" ")

        match len(name_list):
            case 1:
                #only first or last name since key has no whitespace
                assert name == name_key, "just a check"
                self.__handleOneName(name)
            case 2:
                #formatted correctly, add to dict
                host = self.__add(name, name_list, name_key)
                if cohostExist:
                    host.voteCoHost(cohost)
                return #done
            case _:
                #here we would want to check for incorrect parsing if names aren't two words
                return
    

    def total_votes(self):
        """Return list sorted by vote counts
        type --> [(name, votes), (name, votes) ...] in descending order
        """
        
        vote_counter = [(ele[1].name, ele[1].voteCount()) for ele in self.hosts.items()]
        vote_counter = sorted(vote_counter, key=lambda x: x[1], reverse=True)
        return vote_counter

    def __str__(self):
        return "\n".join([str(x) for x in self.hosts.values()])
        

