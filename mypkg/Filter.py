def _intersect(groupA, groupB):
    return [item for item in groupA if item in groupB]
def _union(groupA, groupB):
    elems = set(groupA)
    elems.update(groupB)
    return list(elems)

# + means or
# * means and

class Filter(object):
    def __mul__(self, other):
        ret = Filter(None)
        ret._set((self, other), 'and')
        return ret
    
    def __add__(self, other):
        ret = Filter(None)
        ret._set((self, other), 'or')
        return ret
    
    def __init__(self, stencil):
        self.stencil = stencil
        self.operation = None
        self.filters = None
    
    def _set(self, filters, operation):
        self.filters = filters
        self.operation = operation

    def apply(self, propToValToObjects):
        if self.filters == None:
            # Leaf!
            return self._applyLeaf(propToValToObjects)
        else:
            # Node
            (left, right) = self.filters
            leftMatches = left.apply(propToValToObjects)
            rightMatches = right.apply(propToValToObjects)
            matches = None
            if self.operation == 'and':
                matches = _intersect(leftMatches, rightMatches)
            elif self.operation == 'or':
                matches = _union(leftMatches, rightMatches)
            return matches
            
    
    def _applyLeaf(self, propToValToObjects):
        matches = None
        for prop in self.stencil:
            val = self.stencil[prop]
            if not prop in propToValToObjects:
                # No entries even have this property
                return []
            if not val in propToValToObjects[prop]:
                # No entries have this value
                return []
            
            candidates = propToValToObjects[prop][val]

            if matches == None:
                # This is the first property
                matches = candidates
                continue

            # Use intersection so we can keep only those that maintain all filters
            matches = self._intersect(matches, candidates)
            if len(matches) == 0:
                return []
        return matches
    
    def __str__(self):
        if (self.filters == None):
            # Leaf
            return str(self.stencil)
        else:
            (left, right) = self.filters
            return '(' + str(left) + ' ' + self.operation + ' ' + str(right) + ')'
            