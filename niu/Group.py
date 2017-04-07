class Group:
    def __init__(self, id, info):
        self.id = id
        self.info = info

        # Extract size from info
        if 'size' in info:
            self.size = info['size']
        else:
            self.size = None
        
        # Extract minsize from info
        if 'minsize' in info:
            self.minsize = info['minsize']
        else:
            self.minsize = 0
        
        self.variables = []
    
    def addVar(self, var):
        self.variables.append(var)
    
    def genConstraints(self):
        constraints = []
        
        # Constrain size of group
        if self.size != None:
            constraints.append(sum(self.variables) >= self.size)
        
        # Impose minimum size of group
        if self.minsize != None and self.minsize != 0:
            constraints.append(sum(self.variables) >= self.minsize)
        
        return constraints