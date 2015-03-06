


import sys
pred = [float(line) for            line in file('pred.txt').readlines()]
test = [float(line.split()[0]) for line in file(sys.argv[1], 'r')]

acc = 0
for a, b in zip(pred, test):
    acc += abs(a - b)
print "%.4f" % (acc / float(len(pred)))
