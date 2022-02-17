import math

def stot(sec):
    if (sec == 0.6):
        return 1
    if (sec == 1.8):
        return 3
    if (sec == 3):
        return 5
    if (sec == 5):
        return 9
    if (sec == 7):
        return 12
    if (sec == 10):
        return 17
    if (sec == 15):
        return 25
    if (sec == 20):
        return 34
    if (sec == 24):
        return 41
    if (sec == 30):
        return 50
    if (sec == 45):
        return 75
    if (sec == 60):
        return 100
    if (sec == 90):
        return 150
    if (sec == 120):
        return 200
    if (sec == 300):
        return 500
    else:
        return math.floor(sec/0.6)

def ttos(tick):
    return tick * 0.6