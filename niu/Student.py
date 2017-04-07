import pulp
import Utils

class Student:
    def __init__(self, id, info, groups):
        self.id = id
        self.info = info
    
        self.allVariables = []
        self.groupIDToVariable = {}
        
        for group in groups:
            var = pulp.LpVariable(Utils.encodeVarName(id, group.id), lowBound=0, cat='Integer')
            self.allVariables.append(var)
            self.groupIDToVariable[group.id] = var
            group.addVar(var)
        
    def getVar(self, gid):
        var = self.groupIDToVariable[gid]
        return var
    
    def genConstraints(self):
        constraints = []
        
        # Must be in exactly one group
        constraints.append(sum(self.allVariables) == 1)
        # ^ low bound is 0. Thus, only need one constraint
        
        return constraints