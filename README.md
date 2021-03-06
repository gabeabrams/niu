# niu
Grouping and pairing library

## Guide
### 1. Set up lists of students and groups
These lists should be dictionaries with properties of the students (name, id, etc) and groups (name, type, etc). 

Define a group's maximum size by adding a property: group['size']. Default: unlimited.<br>
Define a group's minimum size by adding a property: group['minsize']. Default: 0.

### 2. Define goal groups 
The algorithm takes a list of goal groups [goalgroup0, goalgroup1, ...]. If groups cannot be created given the goals defined in goalgroup0, the algorithm will try goalgroup1, then goalgroup2, etc.

Goals are constraints on groups (ex: everyone should have the same age). See below for a list of types of constraints that can be applied.

#### GroupFilter Goal
Applies a Filter on all students to get the list of students affected by this goal. Then applies another Filter on all groups to get a list of acceptable groups. This goal requires that all students affected by this goal end up in an acceptable group. Filters are defined in the following section.

Example use case: all students with `diet="vegetarian"` should go into groups with `meal="lasagna"`.

#### MinSimilar Goal
For a given `groupFilter`, `propertyname`, and `cutoff`: applies `groupFilter` to get the list of groups affected by this goal. For affected groups, requires that at least `cutoff` students share the same value for `propertyname`.

Cutoff can be an integer or a dictionary (group size => cutoff). If a cutoff value is -1, the default value of `group size` will be applied.

Example use case: for groups where `type="studytogether"` and `size=4`, at least 3 of the students should have the same value for property `location`.

#### MaxSimilar Goal
For a given `groupFilter`, `propertyname`, and `cutoff`: applies `groupFilter` to get the list of groups affected by this goal. For affected groups, requires that at most `cutoff` students share the same value for `propertyname`.

Cutoff can be an integer or a dictionary (group size => cutoff). If a cutoff value is -1, the default value of 1 will be applied.

Example use case: for groups wher `type="diversitymeeting"`, at most 2 students can have the same value for property `firstlanguage`.

### 3. Run algorithm
Use `solve(students, groups, goalgroups)`:

```
students = [student1, student2, ...]
groups = [group1, group2, ...]
goalgroups = [ [goal0a, goal0b, ...], [goal1a, goal1b, ...], ...]
```

The algorithm will execute using (students, groups, goalgroups[0]) then (students, groups, goalgroups[1]) if the first execution fails, and so on.

### 4. Interpret results
If `None` was returned, no groups could be formed given the goalgroups.

If groups could be created, a list of groups is returned: `[group1, group2, ...]` where a group is a dictionary defined as follows:

```
group['students'] = [studentInfo, studentInfo, ...]
group['info'] = groupInfo
```

The studentInfo and groupInfo objects are the same objects that were passed into `solve()`.