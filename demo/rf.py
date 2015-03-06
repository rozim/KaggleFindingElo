#!/usr/bin/python
# Random Forest demo.

import sklearn.ensemble

r = sklearn.ensemble.RandomForestRegressor()

x = [
    [10.0, 0.0],
    [20.0, 1.0],
    [30.0, 0.5]
    ]

y = [1.0, 2.0, 3.0]
r.fit(x, y)
print r.predict([4.0, 0.9])
