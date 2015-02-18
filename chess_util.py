
# Simplify the FEN string by stripping out the last 2 fields (half move clock and full move #)
# under the assumption that these fields are not signifcant in distinguishing positions when
# we want a set of unique positions.
def SimplifyFen(fen):
    return ' '.join(fen.split()[0:4])
