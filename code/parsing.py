"""
Demo on a cool way to parse files
"""

field_types = [str, str, int, float]
field_names = ['first', 'last', 'age', 'weight']

def parse_line(l):
    field_values = l.split(',')
    return dict((fn, ft(fv)) for fn,ft,fv\
                in zip(field_names, field_types, field_values))

def parse(filename):
    return [parse_line(l) for l in open(filename)]
