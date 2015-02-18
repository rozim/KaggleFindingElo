import sys
from string import Template
import glob

s = Template(file('doit.template').read())

for i in xrange(1, 50001):
    event = '%05d' % i
    with file('%s.html' % event, 'w') as out:
        out.write(s.substitute({'EVENT': event, 'PGN': file('../pgn/%s.pgn' % event).read()}))
