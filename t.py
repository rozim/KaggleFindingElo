

class C(object):
    def __init__(self, m):
        self._m = m

    x = property(lambda me: me._m['z'])

c = C({'z': 213})
print c.x
