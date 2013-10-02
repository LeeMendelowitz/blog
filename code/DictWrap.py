class DictWrap(object):
    """
    Class to wrap a python dictionary.
    This helps with tab completion for object introspection in IPython

        myD = {'one' : 1, 'two' : 2}
        d = DictWrap(myD)

    Now in IPython you can inspect and autocomplete with d.o<TAB> 
    """

    def __init__(self, d):
        """
        Construct a DictWrap instance from a python dictionary d
        """
        self._d = d
        for k,v in d.iteritems():
            setattr(self, k, v)
