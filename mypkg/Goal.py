import pulp

class GoalTypes:
    # Goal types
    GROUP_FILTER = 'group_filter'
    # ^ Data must be (studentFilter, groupFilter) where all students matching studentFilter must be placed into groups matching the groupFilter

    MIN_SIMILAR = 'min_similar'
    # ^ data should be tuple (groupFilter, "propertyname", X) where at least X people in each group share the same value for propertyname
    # X can also be a dictionary (groupFilter, group size => min # people in each group)

    MAX_SIMILAR = 'max_similar'
    # ^ data should be tuple (groupFilter, "propertyname", X) where at most X people in each group share the same value for propertyname
    # X can also be a dictionary (group size => max # people in each group that share a value)

# Goal class
class Goal:

    def __init__(self, goalType, data):
        self.goalType = goalType
        self.data = data
    
    def genConstraints(self, dataBox):
        constraints = []
        
        # Filter goal
        if self.goalType == GoalTypes.GROUP_FILTER:
            (studentFilter, groupFilter) = self.data
            students = dataBox.filterStudents(studentFilter)
            groups = dataBox.filterGroups(groupFilter)

            if len(students) > 0:
                if len(groups) == 0:
                    print "Could not find groups that match filter: " + str(groupFilter) + ". Impossible to match."
                    return None

                for student in students:
                    variables = []
                    for group in groups:
                        variables.append(student.getVar(group.id))
                    constraints.append(sum(variables) >= 1)
        
        # Similarity goals
        elif self.goalType == GoalTypes.MIN_SIMILAR or self.goalType == MGoalTypes.AX_SIMILAR:
            PLACEHOLDER = -1
            
            # Pre-process in self.data
            (groupFilter, propertyname, cutoff) = self.data
            if cutoff == None:
                cutoff = PLACEHOLDER
            
            # Function to get cutoff for sepecific group size
            def _getCutoff(groupSize):
                ret = PLACEHOLDER
                
                if cutoff != PLACEHOLDER:
                    # Look for value for this group size
                    
                    # If cutoff is dictionary, look up group size
                    if type(cutoff) is dict:
                        if groupSize in cutoff:
                            ret = cutoff[groupSize]
                        else:
                            # group size not in dictionary
                            return None # caller should interpret this as "no restriction
                    # If cutoff is same for all groups (not dict), just return that
                    else:
                        ret = cutoff
                        
                if ret == PLACEHOLDER and self.goalType == GoalTypes.MIN_SIMILAR:
                    # Replace placeholder with group size (everyone should be similar)
                    return groupSize
                elif ret == PLACEHOLDER and self.goalType == GoalTypes.MAX_SIMILAR:
                    # Replace placeholder with 1 (nobody should be similar)
                    return 1
                else:
                    return ret
            
            # Grab clicks (groups of students that are similar based on propertyname)
            clicks = dataBox.getStudentsWhoShareProperty(propertyname)
            
            # Filter groups (if applicable)
            groupsOfInterest = None
            if groupFilter == None:
                groupsOfInterest = dataBox.getGroups()
            else:
                groupsOfInterest = dataBox.filterGroups(groupFilter)
            for group in groupsOfInterest:
                M = group.size
                if M == None:
                    M = len(dataBox.getStudents()) # If no group size, intrinsic limit is # students
                
                cutoff = _getCutoff(group.size)
                if cutoff == None:
                    # No restriction, don't continue, don't add constraints
                    continue
                    
                if self.goalType == GoalTypes.MIN_SIMILAR and cutoff == 0:
                    print "Cannot apply min similarity constraint when minimum similar is " + str(cutoff) + ". Constraint on property " + propertyname
                    continue
                
                if self.goalType == GoalTypes.MAX_SIMILAR and group.size != None and (cutoff > group.size or cutoff == 0):
                    print "Cannot apply max similarity constraint when maximum similar is " + str(cutoff) + ". Constraint on property " + propertyname
                    continue
                
                # MIN_SIMILAR process:
                # cutoff = minimum number of similar people required to approve group
                # for each group:
                #   for each click:
                #     > clickCountVar = sum(variables) --- the count of people in this click in this group
                #     > clickSatVar = 1 only if clickCountVar >= minSimilar --- clickSatVar is 1 only if this click satisfies goal for this group
                #          ^ do this with 2 constraints: minSimilar <= clickCountVar + M * (1 - clickSatVar) and minSiilar > clickCountVar - M * clickSatVar
                #   require that at least one satVar is 1
                #   > constraint: sum(clickSatVar) > 0
                if self.goalType == GoalTypes.MIN_SIMILAR:
                    satVariables = []
                    for i in range(len(clicks)):
                        click = clicks[i]
                        # Create click count var
                        variables = []
                        for student in click:
                            var = student.getVar(group.id)
                            variables.append(var)
                        clickCountVar = pulp.LpVariable(str(group.id) + '_minclickcount_' + str(i), lowBound=0, cat='Integer')
                        constraints.append(clickCountVar == sum(variables))
                        # Create click sat var
                        clickSatVar = pulp.LpVariable(str(group.id) + '_minclicksat_' + str(i), 0, 1, cat='Integer')
                        constraints.append(clickSatVar * M <= clickCountVar - cutoff + M)
                        constraints.append(clickSatVar * M >= clickCountVar - cutoff + 1) 
                        satVariables.append(clickSatVar)

                    # Require at least one sat var is true
                    constraints.append(sum(satVariables) >= 1)
                
                # MAX_SIMILAR process:
                # cutoff = maximum number of similar people permitted to approve a group
                # for each group:
                #   for each click:
                #     > clickCountVar = sum(variables) --- the count of people in this click in this group
                #     > constraint: clickCountVar < cutoff
                if self.goalType == GoalTypes.MAX_SIMILAR:
                    for i in range(len(clicks)):
                        click = clicks[i]
                        # Create click count variable
                        variables = []
                        for student in click:
                            var = student.getVar(group.id)
                            variables.append(var)
                        constraints.append(sum(variables) <= cutoff)
            
        return constraints