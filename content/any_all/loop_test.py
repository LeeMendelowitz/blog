class Obj(object):
    
    def __init__(self, num):
        self.g = (i for i in range(num))

    def __iter__(self):
        print 'Iter!!'
        return self.g

o10 = Obj(10)
o2 = Obj(2)

print 'looping'
for i in o2:
    print i
