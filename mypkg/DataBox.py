class DataBox:
    def __init__(self, students, groups):
        self.allStudents = students
        self.allGroups = groups
        
        self.groupsByProp = {}
        for group in groups:
            for prop in group.info:
                val = group.info[prop]
                
                if not prop in self.groupsByProp:
                    self.groupsByProp[prop] = {}
                if not val in self.groupsByProp[prop]:
                    self.groupsByProp[prop][val] = []
                self.groupsByProp[prop][val].append(group)
        
        self.studentsByProp = {}
        for student in students:
            for prop in student.info:
                val = student.info[prop]
                
                if not prop in self.studentsByProp:
                    self.studentsByProp[prop] = {}
                if not val in self.studentsByProp[prop]:
                    self.studentsByProp[prop][val] = []
                self.studentsByProp[prop][val].append(student)
        
        
    def getStudents(self):
        return self.allStudents

    def getGroups(self):
        return self.allGroups
    
    def _filter(self, filter, mapping):
        return filter.apply(mapping)

    def filterStudents(self, filter):
        return self._filter(filter, self.studentsByProp)
    def filterGroups(self, filter):
        return self._filter(filter, self.groupsByProp)
    
    def getStudentsWhoShareProperty(self, propertyname):
        # Returns a list of arrays where each array contains students that have the same value for that property
        out = []
        
        for val in self.studentsByProp[propertyname]:    
            out.append(self.studentsByProp[propertyname][val])
            
        return out