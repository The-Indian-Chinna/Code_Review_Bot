# GENERAL TEST
def forLoop():
    x = 0
    y = 1
    for z in range(0, 3):
        y = 2
        x = x + y
        y = 1
    print(x)
    x = 0
    print(x)
    print(y)


def check():
    moving = True
    test = True
    while moving == True:
        moving = False
        for z in range(0, 3):
            if test == True:
                moving = True
                test = False
            else:
                print(moving)


def topNCommon(filename, N):
    commonN = []
    ngramDict = getDict(filename)
    ngramDict = {
        keys: value
        for keys, value in sorted(ngramDict.items(), key=lambda item: item[1], reverse=True)
    }
    count = 0
    for gram, counter in ngramDict.items():
        if count <= N - 1:
            commonN.append((gram, counter))
            count = count + 1
        else:
            count = count + 1
            break
    return commonN
