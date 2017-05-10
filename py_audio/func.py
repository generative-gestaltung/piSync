import math

PI = math.pi

def sign (v):
    if (v>0):
        return 1
    return -1

def sq (ph):
    return sign(math.sin(ph))

def saw (ph):
    return (ph%(2*PI)) / PI - 1


def pulse (ph, pw):
    
    val = saw(ph)
    if (val>pw):
        return 1
    return -1
