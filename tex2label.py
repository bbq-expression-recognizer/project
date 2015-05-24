class Mapper:
    """Provides mapping between tex symbol and label.

    Label is non-negative integer.
    Mapping is unique if input file is the same.
    Input file is whitespace-separated tex symbols.

    Example usage:
    foo = Mapper('texsyms.txt')
    print foo.tex2label('\\gt')
    print foo.label2tex(42)
    """
    def __init__(self, filename):
        f = open(filename)
        self.syms = f.read().split()
        f.close()
        self.syms.sort()
        self.inv = {}
        for i in xrange(len(self.syms)):
            self.inv[self.syms[i]] = i

    def tex2label(self, sym):
        if not sym in self.inv:
            return None
        return self.inv[sym]

    def label2tex(self, label):
        return self.syms[label]

if __name__ == '__main__':
    syms = Mapper('texsyms.txt').syms
    for i in xrange(len(syms)):
        print i, syms[i]
