import re

def getrange(rstr: str):
    (mins,maxs) = re.sub(r'[\[\]]','',rstr).split(',')

    if maxs == '':
        maxs = mins

    mini = int(mins)
    maxi = int(maxs)+1

    return range(mini, maxi)
    


def remove_null_conf(prof: dict):
    retprof = {}

    for k in prof:
        if prof[k] is None:
            continue

        if type(prof[k]) is dict and len(prof[k]) > 0:
            retprof[k] =  remove_null_conf(prof[k])
        elif len(prof[k]) > 0:
            retprof[k] = prof[k]
        else:
            pass

    return retprof

