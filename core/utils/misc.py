
class Context(dict):
    def __init__(self, *argv, **kw):
        super(Context, self).__init__(*argv, **kw)
        self.update([
            (d, getattr(self, d))
            for d in self.__class__.__dict__ if not d.startswith('_')
        ])

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k.args[0])

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k.args[0])

    def __repr__(self):
        return '<Context ' + dict.__repr__(self) + '>'


class SafeContext(Context):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            return None
