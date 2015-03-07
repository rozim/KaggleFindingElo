



def PoorMansIntegration(x1, x2):
    if x1 == x2:
        return 0
    assert x1 < x2

    epsilon = 0.001    
    if x1 < 0 and x2 > 0:
        return PoorMansIntegration(x1, -epsilon) + PoorMansIntegration(+epsilon, x2)
    if x1 == 0:
        x1 = epsilon
    elif x2 == 0:
        x2 = -epsilon


    size = 10.0
    isize = int(size)
    width = 1.0 / size
    res = 0
    steps = 0
    print x1, x2, int(x1 * isize), int(x2 * isize)
    for x in (x/size for x in range(x1 * isize, (x2 * isize) + 1)):

        res += (1.0 / (1.0 + x)) * width
    return res

print PoorMansIntegration(-150, -50)
print PoorMansIntegration(-50, 50)
print PoorMansIntegration(50, 150)
print PoorMansIntegration(100, 200)
print PoorMansIntegration(150, 250)


    
    
    
