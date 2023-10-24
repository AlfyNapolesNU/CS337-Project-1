class Hosts:

    def __init__(self):
        #k: host name: lower case, no spaces
        #v: object of class Person
        self.hosts = {}
    

    def __checkName__(self, name):
        """Check for name when single string
        - could be combined first/last or just first or just last
        """
        for k in self.hosts.keys():
            # case just first/last
            if 


    
    def add_host(self, name):
        """ Public method 
        - takes a host name as a string & checks for host name in dictionary of hosts
        - adds new host to dict with 1 vote OR increments number votes
        - handle only first name, last name or name not seperated? nicknames?
        - success code?
        """
        if not isinstance(name, str):
            #remove whitespace
            name = name.strip()
            #split by whitespace: firstname, lastname or firstname & capitalize
            name_list = [x.capitalize() for x in name.split(" ")]
            
            #match by number of names
            match len(name_list):
                case 1:
                    #only first or last name or not seperated by white space
                    name = name[0]
                    #if issue add algorithm for splitting name?
                case 2:
                    #first and last name
                    name = " ".join(name_list)
                    #add to dict, if not present default to 1 vote
                    self.hosts[name] = self.hosts.get(name, 0) + 1
                
                case _:
                    #other?
