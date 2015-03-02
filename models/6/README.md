A ridiculous and simple submission based on simple-header-submission.py and study-header.py.

Data came from 1.3M games from TWIC that had the test set filtered out.

The prediction code is simply:

def Predict(ply, result):
    if result == '1-0':
        return (2345, 2221)
    elif result == '0-1':
        return (2202, 2335)
    elif result == '1/2-1/2':
        if ply < 30:
            return (2363, 2384)
        else:
            return (2346, 2357)

On the training set the score was 208.
When submitted: score was 208 and I am in place 98 so the top 100 out of 133.
So there is promise in separate models based on result and game length.