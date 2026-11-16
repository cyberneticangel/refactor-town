def summarize(l):
    x = []
    for i in range(len(l)):
        if l[i] >= 0:
            x.append(l[i])
    t = 0
    for i in range(len(x)):
        t = t + x[i]
    if len(x) == 0:
        return {"count": 0, "total": 0, "average": 0, "highest": None}
    h = x[0]
    for i in range(len(x)):
        if x[i] > h:
            h = x[i]
    a = t / len(x)
    return {"count": len(x), "total": t, "average": a, "highest": h}
