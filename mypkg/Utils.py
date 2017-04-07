# Helpers

def encodeVarName(sid, gid):
    return str(sid) + '_' + str(gid)
def decodeVarName(varName):
    try:
        parts = varName.split('_')
        return (int(parts[0]), int(parts[1]))
    except ValueError:
        return None
def multAll(lst):
    if len(lst) == 0:
        return 0
    
    out = lst[0]
    for i in range(1,len(lst)):
        out *= lst[i]
    return out