import pulp
from Group import Group
from Student import Student
from DataBox import DataBox
import Utils

def solve(studentInfos, groupInfos, goalGroups):
    # Set up groups
    groups = []
    gidToGroupInfo = {}
    nextGID = 1
    for group in groupInfos:
        groupObj = Group(nextGID, group)
        if groupObj.size != None and groupObj.size == 0:
            # Skip groups with no room
            continue
        groups.append(groupObj)
        gidToGroupInfo[groupObj.id] = group
        nextGID += 1
        
    # Set up students
    students = []
    sidToStudentInfo = {}
    nextSID = 1
    for student in studentInfos:
        studentObj = Student(nextSID, student, groups)
        students.append(studentObj)
        sidToStudentInfo[studentObj.id] = student
        nextSID += 1
    
    # Set up data box
    dataBox = DataBox(students, groups)
    
    # Run for each set of goals until 'Optimal' is found, or return None    
    for i in range(len(goalGroups)):
        goals = goalGroups[i]
        problem = pulp.LpProblem("Group Membership Problem", pulp.LpMaximize)
        
        # Add student constraints
        failedAddingConstraints = False
        for student in students:
            constraints = student.genConstraints()
            if constraints == None:
                failedAddingConstraints = True
                break
            for constraint in constraints:
                problem += constraint
        
        # Add group constraints
        for group in groups:
            constraints = group.genConstraints()
            if constraints == None:
                failedAddingConstraints = True
                break
            for constraint in constraints:
                problem += constraint

        # Add goal constraints
        for goal in goals:
            constraints = goal.genConstraints(dataBox)
            if constraints == None:
                failedAddingConstraints = True
                break
            for constraint in constraints:
                problem += constraint
                
        if failedAddingConstraints:
            print "> Goal group " + str(i) + " failed because constraints couldn't be generated. Trying next goal group..."
            continue
        
        # Objective function
        # TODO: add objective function
        
        # Attempt to solve
        problem.solve()
        
        solved = pulp.LpStatus[problem.status] == 'Optimal'
        if solved:
            print "> Successful with goal group " + str(i)
            output = [None for i in range(len(groups))]
            #output = [{"students": [students], "group": groupinfo}, ...]
            for variable in problem.variables():
                if variable.name == '__dummy':
                    continue
                if variable.varValue == 0:
                    continue
                ret = Utils.decodeVarName(variable.name)
                if ret == None:
                    continue
                (sid,gid) = ret
                student = sidToStudentInfo[sid]
                group = gidToGroupInfo[gid]
                
                index = gid - 1
                if output[index] == None:
                    output[index] = {}
                    output[index]['students'] = []
                    output[index]['info'] = group
                output[index]['students'].append(student)
                
            return output
        else:
            print "> Goal group " + str(i) + " was too strict. Trying next goal group..."
    print "> All goal groups were too strict. No groups could be created"
    return None