def permutation(pool):
        if (len(pool) == 0):
            return []
        if (len(pool) == 1):
            return [pool]
        l = []
        for i in range(len(pool)):
            m  = pool[i]
            remLst = pool[:i] + pool[i+1:]
            for p in permutation(remLst):
                l.append([m] + p)
        return l

data = [1,2,3,4,5,6,7]
print(permutation(data))