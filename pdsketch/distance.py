from pdsketch import PDPoint

def l_inf(a: PDPoint, b: PDPoint)->float:
    """
    Compute the l-infinity distance between `a` and `b`.
    """
    return max(abs(x-y) for x,y in zip(a, b))

def l_p(a:PDPoint, b:PDPoint, p:float)->float:
    """
    Compute the l_`p` distance between `a` and `b`
    """
    return (sum((abs(x-y))**p for x,y in zip(a, b)))**(1/p)